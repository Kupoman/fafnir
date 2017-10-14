import panda3d.core as p3d


class StageGather:
    def __init__(self, data_manager):
        self.data = data_manager
        self.is_enabled = False

        self.shader_gather = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex='shaders/build_mesh_cache.vert',
            geometry='shaders/build_mesh_cache.geom',
            fragment='shaders/generate_primary_intersections.frag'
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

    def enable(self):
        if self.is_enabled:
            return
        self.is_enabled = True

        self.data.np_scene_root.set_attrib(self.color_blend_attrib)
        self.data.np_scene_root.set_attrib(self.transparency_attrib)
        self.data.np_scene_root.set_attrib(self.alpha_test_attrib)
        self.shader_saved = self.data.np_scene_root.get_shader()
        self.data.np_scene_root.set_shader(self.shader_gather)

        self.data.np_scene_root.set_shader_input('buffer_vertices', self.data.buffer_vertices)
        self.data.np_scene_root.set_shader_input('buffer_primitives', self.data.buffer_primitives)

        # Setup RTT
        fb_prop = p3d.FrameBufferProperties()
        fb_prop.set_rgba_bits(32, 32, 32, 32)
        fb_prop.set_float_color(True)
        fb_prop.set_depth_bits(32)
        win_prop = p3d.WindowProperties().size(*self.data.window_size)
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
        self.data.np_scene_root.hide(self.data.mask_draw)

    def disable(self):
        if not self.is_enabled:
            return
        self.is_enabled = False

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
            nodepath.set_shader_input('window_width', self.data.window_size[0])
