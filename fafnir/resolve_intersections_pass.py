import os

import panda3d.core as p3d

from panda3d_render_pass import RenderPass


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')


class ResolveIntersectionsPass(RenderPass):
    def __init__(
            self,
            name,
            graphics_context,
            texture_intersections,
            buffer_meshes,
            buffer_materials,
            material_records,
    ):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(True)
        fb_props.set_rgba_bits(8, 8, 8, 0)

        self.material_records = material_records
        self._fsq = self._make_fullscreen_quad()
        scene = self._make_draw_path()
        super().__init__(
            name,
            **graphics_context,
            scene=scene,
            frame_buffer_properties=fb_props,
            clear_color=p3d.LColor(0.0, 0.0, 0.0, 0.0),
            shader=p3d.Shader.load(
                p3d.Shader.SL_GLSL,
                SHADER_DIR + 'fsq.vert',
                SHADER_DIR + 'resolve_intersections.frag'
            ),
        )

        self._root.set_shader_input('texture_intersections', texture_intersections)
        self._root.set_shader_input('buffer_meshes', buffer_meshes.get_texture())
        self._root.set_shader_input('buffer_materials', buffer_materials.get_texture())

    def _make_fullscreen_quad(self):
        tris = p3d.GeomTristrips(p3d.GeomEnums.UH_static)
        tris.add_next_vertices(4)
        vdata = p3d.GeomVertexData(
            'abc',
            p3d.GeomVertexFormat.get_empty(),
            p3d.GeomEnums.UH_static
        )

        geom = p3d.Geom(vdata)
        geom.add_primitive(tris)
        geom.set_bounds(p3d.OmniBoundingVolume())

        node = p3d.GeomNode('Resolve Pass FSQ')
        node.add_geom(geom)

        return p3d.NodePath(node)

    def _make_draw_path(self):
        cb_node = p3d.CallbackNode('Intersection Draw Callback')
        cb_node_path = p3d.NodePath(cb_node)
        cb_node_path.set_shader_input('instance_id', 1)

        def cull_callback(callback_data):
            for instance in cb_node_path.children:
                instance.detach_node()

            for i, record in enumerate(self.material_records):
                placeholder = cb_node_path.attach_new_node('placeholder')
                placeholder.set_texture(record.texture)
                placeholder.set_shader_input('instance_id', i)
                instance = self._fsq.instance_to(placeholder)

            callback_data.upcall()

        cb_node.cull_callback = p3d.PythonCallbackObject(cull_callback)
        return cb_node_path
