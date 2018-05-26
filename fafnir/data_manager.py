import ctypes

import panda3d.core as p3d

from .gpu_buffer import GpuBuffer


class DataManager:
    def __init__(self, scene_root_np, render_np):
        self.np_scene_root = scene_root_np
        self.np_render = render_np

        self.geom_node_paths = []

        self.primitive_count = 0
        self.material_count = 0

        # Materials
        self.material_map = {}

        # Textures
        self.texture_intersections = p3d.Texture()
        self.texture_material_ids = p3d.Texture()

        # Buffers
        self.vertex_stride = 2
        self.buffer_meshes = GpuBuffer('mesh_buffer', 0, p3d.Texture.T_float, p3d.Texture.F_rgba32)
        self.buffer_materials = p3d.Texture()

        # Bitmasks
        self.mask_rtt = 1
        self.mask_draw = 2

        self.update()

    def update(self):
        materials = self.np_scene_root.find_all_materials()
        material_count = materials.get_num_materials()
        if material_count > self.material_count:
            print('Setting material_count to', material_count)
            self.material_count = material_count
            self.buffer_materials.setup_buffer_texture(
                self.material_count * 4,
                p3d.Texture.T_float,
                p3d.Texture.F_rgba32,
                p3d.GeomEnums.UH_dynamic
            )
        material_ram_image = (ctypes.c_float * (material_count * 4 * 4))()
        for i, material in enumerate(materials):
            image_idx = i * 16

            ambient = material.get_ambient()
            material_ram_image[image_idx + 0] = ambient.x
            material_ram_image[image_idx + 1] = ambient.y
            material_ram_image[image_idx + 2] = ambient.z
            material_ram_image[image_idx + 3] = ambient.w

            diffuse = material.get_diffuse()
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
        self.buffer_materials.set_ram_image(material_ram_image)

        self.material_map = {material.name: i for i, material in enumerate(materials)}

        self.geom_node_paths = list(self.np_scene_root.find_all_matches('**/+GeomNode'))

        primitive_count = 0
        for nodepath in self.geom_node_paths:
            nodepath.set_shader_input('primitive_offset', primitive_count)
            for node in nodepath.get_nodes():
                if isinstance(node, p3d.GeomNode):
                    for geom in node.get_geoms():
                        for primitive in geom.get_primitives():
                            primitive_count += primitive.get_num_faces()

        if primitive_count > self.primitive_count:
            print('Setting primitive_count to', primitive_count)
            self.primitive_count = primitive_count
            self.buffer_meshes.resize(self.primitive_count * 3 * self.vertex_stride)
