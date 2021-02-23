import ctypes
import os

from OpenGL import GL as gl

import panda3d.core as p3d
from panda3d_render_pass import RenderPass

import lionrender

from .gpu_buffer import GpuBufferRGBA32F


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')
VERTEX_STRIDE = 4
MATERIAL_STRIDE = 5

class MaterialRecord:
    def __init__(self, material, texture):
        self.material = material
        self.texture = texture

class GeometryPass(RenderPass):
    def __init__(self, name, graphics_context, scene=None, camera=None):
        self.name = name
        self.graphics_context = graphics_context
        self.root_np = p3d.NodePath(name + '_root')
        self.mesh_buffer = GpuBufferRGBA32F(
            'mesh_buffer',
            0,
            graphics_context['window'].get_gsg()
        )
        self.xfb = lionrender.TransformFeedbackBuffer('geometry_xfb', self.mesh_buffer)
        self.material_buffer = GpuBufferRGBA32F(
            'material_buffer',
            0,
            graphics_context['window'].get_gsg()
        )
        self.material_records = []
        self.primitive_count = 0
        self.material_count = 0
        self._default_material = p3d.Material('fafnir_default')

        self._init_xfb()

        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(False)
        super().__init__(
            self.name,
            **graphics_context,
            frame_buffer_properties=fb_props,
            shader=p3d.Shader.load(
                p3d.Shader.SL_GLSL,
                SHADER_DIR + 'build_mesh_cache.vert',
                SHADER_DIR + 'debug.frag',
            ),
            clear_color=p3d.LVector4(0.0, 0.0, 0.0, 1.0),
            scene=self.root_np,
            camera=camera,
        )

        scene.instance_to(self.root_np)
        self._root.set_shader_input('object_id', 0)

    def _init_xfb(self):
        def attach_new_callback(prop, nodepath, name, callback):
            cb_node = p3d.CallbackNode(name)
            setattr(cb_node, prop, p3d.PythonCallbackObject(callback))
            cb_node_path = nodepath.attach_new_node(cb_node)
            return cb_node_path

        def attach_new_cull_callback(nodepath, name, callback):
            return attach_new_callback('cull_callback', nodepath, name, callback)

        def update(callback_data):
            self._iterate_geometry()
            callback_data.upcall()

        attach_new_cull_callback(
            self.root_np,
            self.name + '_xfb_resize',
            update
        )

        self.root_np.set_shader_input('material_index', 0)
        self.xfb.attach(self.root_np)

    def _update_material_buffer_size(self, material_count):
        if material_count <= self.material_count:
            return
        self.material_count = material_count
        self.material_buffer.resize(self.material_count * MATERIAL_STRIDE)

    def _update_material_buffer(self):
        if len(self.material_records) == 0:
            return

        material_ram_image = (ctypes.c_float * (len(self.material_records) * MATERIAL_STRIDE * 4))()
        for i, record in enumerate(self.material_records):
            material = record.material
            image_idx = i * MATERIAL_STRIDE * 4

            ambient = material.get_ambient()
            material_ram_image[image_idx + 0] = ambient.x
            material_ram_image[image_idx + 1] = ambient.y
            material_ram_image[image_idx + 2] = ambient.z
            material_ram_image[image_idx + 3] = ambient.w

            diffuse = material.get_base_color()
            material_ram_image[image_idx + 4] = diffuse.x
            material_ram_image[image_idx + 5] = diffuse.y
            material_ram_image[image_idx + 6] = diffuse.z
            material_ram_image[image_idx + 7] = diffuse.w

            emission = material.get_emission()
            material_ram_image[image_idx + 8] = emission.x
            material_ram_image[image_idx + 9] = emission.y
            material_ram_image[image_idx + 10] = emission.z
            material_ram_image[image_idx + 11] = emission.w

            specular = material.get_specular()
            material_ram_image[image_idx + 12] = specular.x
            material_ram_image[image_idx + 13] = specular.y
            material_ram_image[image_idx + 14] = specular.z
            material_ram_image[image_idx + 15] = material.get_shininess()

            material_ram_image[image_idx + 16] = 0
            material_ram_image[image_idx + 17] = 0
            material_ram_image[image_idx + 18] = 0
            material_ram_image[image_idx + 19] = 0

        self.material_buffer.get_texture().set_ram_image(material_ram_image)

    def _generate_material_record(self, nodepath):
        materials = nodepath.find_all_materials()
        material = materials[0] if materials else self._default_material
        textures = nodepath.find_all_textures()
        texture = textures[-1] if textures else 0
        return MaterialRecord(material, texture)

    def _iterate_geometry(self):
        geom_node_paths = list(self.root_np.find_all_matches('**/+GeomNode'))

        material_count = 0
        self.material_records.clear()

        for nodepath in geom_node_paths:
            nodepath.set_shader_input('object_id', material_count)
            self.material_records.append(self._generate_material_record(nodepath))
            material_count += 1

        self._update_material_buffer_size(material_count)
        self._update_material_buffer()

    def _extract_buffer(self, texture):
        gsg = self.graphics_context['window'].get_gsg()
        self.graphics_context['engine'].extract_texture_data(texture, gsg)
        view = memoryview(texture.get_ram_image()).cast('f')
        return view

    def extract_mesh_cache(self):
        return self._extract_buffer(self.mesh_buffer.get_texture())

    def extract_material_cache(self):
        return self._extract_buffer(self.material_buffer.get_texture())
