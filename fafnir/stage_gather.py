import panda3d.core as p3d
from OpenGL import GL as gl


def attach_new_callback_node(nodepath, name, callback):
    cb_node = p3d.CallbackNode(name)
    cb_node.set_draw_callback(p3d.PythonCallbackObject(callback))
    cb_node_path = nodepath.attach_new_node(cb_node)
    return cb_node_path


class StageGather:
    def __init__(self, data_manager):
        self.data = data_manager
        self.is_enabled = False

        self.shader_gather = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex='shaders/build_mesh_cache.vert',
            fragment='shaders/debug.frag',
        )
        self.shader_primary_rays = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex='shaders/generate_primary_intersections.vert',
            fragment='shaders/generate_primary_intersections.frag',
        )
        self.shader_saved = None

        self.camera = None
        self.rtt_buffer = None

        self.color_blend_attrib = p3d.ColorBlendAttrib.make(
            p3d.ColorBlendAttrib.M_add,
            p3d.ColorBlendAttrib.O_one,
            p3d.ColorBlendAttrib.O_zero,
            p3d.LColor(1.0, 1.0, 1.0, 1.0)
        )
        self.transparency_attrib = p3d.TransparencyAttrib.make(p3d.TransparencyAttrib.M_none)
        self.alpha_test_attrib = p3d.AlphaTestAttrib.make(p3d.AlphaTestAttrib.M_none, 1.0)

        self.xfb_cb_paths = []
        self.xfb_active = False
        self.ray_path = None

    def setup_xfb(self):
        bin_manager = p3d.CullBinManager.get_global_ptr()
        bin_manager.add_bin('xfb_begin', p3d.CullBinManager.BT_fixed, 5)
        bin_manager.add_bin('xfb_end', p3d.CullBinManager.BT_fixed, 55)

        def begin_callback(callback_data):
            buffer_id = self.data.buffer_meshes.get_buffer_id()
            if buffer_id and not self.xfb_active:
                gl.glEnable(gl.GL_RASTERIZER_DISCARD)
                gl.glBindBufferBase(gl.GL_TRANSFORM_FEEDBACK_BUFFER, 0, buffer_id)
                gl.glBeginTransformFeedback(gl.GL_TRIANGLES)
                self.xfb_active = True

            callback_data.upcall()

        def end_callback(callback_data):
            if self.xfb_active:
                gl.glEndTransformFeedback()
                gl.glBindBufferBase(gl.GL_TRANSFORM_FEEDBACK_BUFFER, 0, 0)
                gl.glDisable(gl.GL_RASTERIZER_DISCARD)
                self.xfb_active = False
            callback_data.upcall()

        begin_path = attach_new_callback_node(self.data.np_render, 'Begin XFB', begin_callback)
        begin_path.set_bin('xfb_begin', 10)

        end_path = attach_new_callback_node(self.data.np_render, 'End XFB', end_callback)
        end_path.set_bin('xfb_end', 10)

        self.xfb_cb_paths = (begin_path, end_path)
        for path in self.xfb_cb_paths:
            path.set_shader(self.shader_gather)
            path.set_shader_input('primitive_offset', 0)
            path.set_shader_input('material_index', 0)
            path.hide(self.data.mask_draw)

    def setup_primary_rays(self):
        def ray_callback(callback_data):
            gl.glDrawTransformFeedback(gl.GL_TRIANGLES, 0)
            callback_data.upcall()

        self.ray_path = attach_new_callback_node(self.data.np_render, 'Primary Rays', ray_callback)
        self.ray_path.set_bin('xfb_end', 20)
        self.ray_path.set_shader(self.shader_primary_rays)
        self.ray_path.set_shader_input('buffer_meshes', self.data.buffer_meshes.get_texture())
        self.ray_path.hide(self.data.mask_draw)

    def setup_render_target(self):
        fb_prop = p3d.FrameBufferProperties()
        fb_prop.set_rgba_bits(32, 32, 32, 32)
        fb_prop.set_float_color(True)
        fb_prop.set_depth_bits(32)
        window_size = [base.win.get_x_size(), base.win.get_y_size()]
        win_prop = p3d.WindowProperties().size(*window_size)
        self.rtt_buffer = base.graphics_engine.make_output(
            base.pipe,
            'Fafnir Gather Stage RTT',
            -100,
            fb_prop,
            win_prop,
            p3d.GraphicsPipe.BF_refuse_window | p3d.GraphicsPipe.BF_size_track_host,
            base.win.get_gsg(),
            base.win
        )
        self.rtt_buffer.add_render_texture(
            self.data.texture_intersections,
            p3d.GraphicsOutput.RTM_bind_or_copy,
            p3d.GraphicsOutput.RTP_color
        )
        self.camera = base.make_camera(
            self.rtt_buffer,
            camName='RTT camera',
            mask=self.data.mask_rtt,
            lens=base.cam.node().get_lens()
        )
        self.camera.reparent_to(self.data.np_scene_root)
        self.camera.node().get_display_region(0).set_sort(1)


    def enable(self):
        if self.is_enabled:
            return
        self.is_enabled = True

        self.setup_xfb()
        self.setup_primary_rays()

        self.data.np_scene_root.set_attrib(self.color_blend_attrib)
        self.data.np_scene_root.set_attrib(self.transparency_attrib)
        self.data.np_scene_root.set_attrib(self.alpha_test_attrib)
        self.shader_saved = self.data.np_scene_root.get_shader()
        self.data.np_scene_root.set_shader(self.shader_gather)

        self.data.np_scene_root.set_shader_input('material_index', 0)

        self.setup_render_target()
        self.data.np_scene_root.hide(self.data.mask_draw)

    def disable(self):
        if not self.is_enabled:
            return
        self.is_enabled = False

        for cb_path in self.xfb_cb_paths:
            cb_path.remove_node()

        if self.ray_path:
            self.ray_path.remove_node()

        if self.shader_saved:
            self.data.np_scene_root.set_shader(self.shader_saved)
        else:
            self.data.np_scene_root.clear_shader()

        if self.rtt_buffer:
            self.rtt_buffer.clear_render_textures()
            base.graphics_engine.remove_window(self.rtt_buffer)
            self.rtt_buffer = None

        if self.camera:
            self.camera.remove_node()
            self.camera = None

    def update(self):
        # Set shader inputs
        material_map = self.data.material_map
        for nodepath in self.data.geom_node_paths:
            try:
                material_index = material_map[nodepath.findMaterial('*').name]
            except AttributeError:
                print('{} has no material'.format(nodepath.getName()))
                material_index = 0
            nodepath.set_shader_input('material_index', material_index)
