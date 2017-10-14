import panda3d.core as p3d


class DataManager:
    def __init__(self, scene_root_np, render_np):
        self.np_scene_root = scene_root_np
        self.np_render = render_np

        self.geom_node_paths = []

        self.window_size = [0, 0]
        self.vertex_count = 0
        self.primitive_count = 0

        # Materials
        self.material_map = {}

        # Textures
        self.texture_intersections = p3d.Texture()
        self.texture_material_ids = p3d.Texture()

        # Buffers
        self.buffer_vertices = p3d.Texture()
        self.buffer_primitives = p3d.Texture()

        # Bitmasks
        self.mask_rtt = 1
        self.mask_draw = 2

        self.update()

    def update(self):
        self.window_size = [base.win.get_x_size(), base.win.get_y_size()]

        materials = self.np_scene_root.find_all_materials()
        self.material_map = {material.name: i for i, material in enumerate(materials)}

        self.geom_node_paths = self.np_scene_root.find_all_matches('**/+GeomNode')

        vertex_count = 0
        primitive_count = 0

        for nodepath in self.geom_node_paths:
            nodepath.set_shader_input('vertex_offset', vertex_count)
            nodepath.set_shader_input('primitive_offset', primitive_count)
            for node in nodepath.get_nodes():
                if isinstance(node, p3d.GeomNode):
                    for geom in node.get_geoms():
                        for primitive in geom.get_primitives():
                            vertex_count += primitive.get_num_vertices()
                            primitive_count += primitive.get_num_faces()

        if vertex_count > self.vertex_count:
            print('Setting vertex_count to', vertex_count)
            self.vertex_count = vertex_count

            self.buffer_vertices.setup_buffer_texture(
                self.vertex_count * 2,
                p3d.Texture.T_float,
                p3d.Texture.F_rgba32,
                p3d.GeomEnums.UH_dynamic
            )

        if primitive_count > self.primitive_count:
            print('Setting primitive_count to', primitive_count)
            self.primitive_count = primitive_count

            self.buffer_primitives.setup_buffer_texture(
                self.primitive_count * 3,
                p3d.Texture.T_int,
                p3d.Texture.F_r32i,
                p3d.GeomEnums.UH_dynamic
            )
