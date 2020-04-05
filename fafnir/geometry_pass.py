import os

from OpenGL import GL as gl

import panda3d.core as p3d
from panda3d_render_pass import RenderPass

from .gpu_buffer import GpuBufferRGBA32F


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')
VERTEX_STRIDE = 4


class GeometryPass(RenderPass):
    def __init__(self, name, graphics_context, scene=None, camera=None):
        self.name = name
        self.graphics_context = graphics_context
        self.root_np = p3d.NodePath(name + '_root')
        self.xfb_active = False
        self.mesh_buffer = GpuBufferRGBA32F(
            'mesh_buffer',
            0,
            graphics_context['window'].get_gsg()
        )
        self.primitive_count = 0
        self._init_xfb(scene)

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

    def _init_xfb(self, scene):
        def attach_new_callback(prop, nodepath, name, callback):
            cb_node = p3d.CallbackNode(name)
            setattr(cb_node, prop, p3d.PythonCallbackObject(callback))
            cb_node_path = nodepath.attach_new_node(cb_node)
            return cb_node_path

        def attach_new_cull_callback(nodepath, name, callback):
            return attach_new_callback('cull_callback', nodepath, name, callback)

        def attach_new_draw_callback(nodepath, name, callback):
            return attach_new_callback('draw_callback', nodepath, name, callback)

        def update(callback_data):
            self._iterate_geometry()
            callback_data.upcall()

        def begin(callback_data):
            buffer_id = self.mesh_buffer.get_buffer_id()
            if buffer_id and not self.xfb_active:
                gl.glEnable(gl.GL_RASTERIZER_DISCARD)
                gl.glBindBufferBase(gl.GL_TRANSFORM_FEEDBACK_BUFFER, 0, buffer_id)
                gl.glBeginTransformFeedback(gl.GL_TRIANGLES)
                self.xfb_active = True
            callback_data.upcall()

        def end(callback_data):
            if self.xfb_active:
                gl.glEndTransformFeedback()
                gl.glBindBufferBase(gl.GL_TRANSFORM_FEEDBACK_BUFFER, 0, 0)
                gl.glDisable(gl.GL_RASTERIZER_DISCARD)
                self.xfb_active = False
            callback_data.upcall()

        bin_manager = p3d.CullBinManager.get_global_ptr()
        bin_manager.add_bin('xfb_begin', p3d.CullBinManager.BT_fixed, 5)
        bin_manager.add_bin('xfb_end', p3d.CullBinManager.BT_fixed, 55)

        path = attach_new_cull_callback(
            self.root_np,
            self.name + '_xfb_resize',
            update
        )
        path.set_bin('xfb_begin', 10)

        path = attach_new_draw_callback(
            self.root_np,
            self.name + '_xfb_begin',
            begin
        )
        path.set_bin('xfb_begin', 11)

        scene.instance_to(self.root_np)
        path = attach_new_draw_callback(
            self.root_np,
            self.name + '_xfb_end',
            end
        )
        path.set_bin('xfb_end', 10)

        self.root_np.set_shader_input('material_index', 0)

    def _update_mesh_buffer_size(self, primitive_count):
        if primitive_count <= self.primitive_count:
            return

        self.primitive_count = primitive_count
        self.mesh_buffer.resize(self.primitive_count * 3 * VERTEX_STRIDE)

    def _iterate_geometry(self):
        geom_node_paths = list(self.root_np.find_all_matches('**/+GeomNode'))

        primitive_count = 0
        for nodepath in geom_node_paths:
            nodepath.set_shader_input('primitive_offset', primitive_count)
            for node in nodepath.get_nodes():
                if isinstance(node, p3d.GeomNode):
                    for geom in node.get_geoms():
                        for primitive in geom.get_primitives():
                            primitive_count += primitive.get_num_faces()

        self._update_mesh_buffer_size(primitive_count)

    def get_mesh_cache(self):
        return self.mesh_buffer.get_texture()

    def extract_mesh_cache(self):
        texture = self.get_mesh_cache()
        gsg = self.graphics_context['window'].get_gsg()
        self.graphics_context['engine'].extract_texture_data(texture, gsg)
        view = memoryview(texture.get_ram_image()).cast('f')
        return view
