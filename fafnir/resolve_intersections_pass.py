import os

from OpenGL import GL as gl
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
            depth_filter_pass,
    ):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(True)
        fb_props.set_rgba_bits(8, 8, 8, 0)
        fb_props.set_depth_bits(24)

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
                SHADER_DIR + 'resolve_intersections.vert',
                SHADER_DIR + 'resolve_intersections.frag'
            ),
            share_depth_with=depth_filter_pass
        )

        self._root.set_shader_input('texture_intersections', texture_intersections)
        self._root.set_shader_input('buffer_meshes', buffer_meshes.get_texture())
        self._root.set_shader_input('buffer_materials', buffer_materials.get_texture())
        self._root.set_shader_input('instance_id', 0)

        self._root.set_depth_test(False)

        self._init_clip_control()

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
        cb_node_path.set_attrib(p3d.DepthTestAttrib.make(p3d.RenderAttrib.MEqual))

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

    def _init_clip_control(self):
        def attach_new_callback(nodepath, name, callback):
            cb_node = p3d.CallbackNode(name)
            cb_node.draw_callback = p3d.PythonCallbackObject(callback)
            cb_node_path = nodepath.attach_new_node(cb_node)
            return cb_node_path

        def begin(callback_data):
            gl.glClipControl(gl.GL_LOWER_LEFT, gl.GL_ZERO_TO_ONE)
            callback_data.upcall()

        def end(callback_data):
            gl.glClipControl(gl.GL_LOWER_LEFT, gl.GL_NEGATIVE_ONE_TO_ONE)
            callback_data.upcall()

        bin_manager = p3d.CullBinManager.get_global_ptr()
        bin_manager.add_bin('clip_control_begin', p3d.CullBinManager.BT_fixed, 5)
        bin_manager.add_bin('clip_control_end', p3d.CullBinManager.BT_fixed, 55)

        path = attach_new_callback(
            self._root,
            self.name + '_clip_control_begin',
            begin
        )
        path.set_bin('clip_control_begin', 11)

        path = attach_new_callback(
            self._root,
            self.name + '_clip_control_end',
            end
        )
        path.set_bin('clip_control_end', 10)
