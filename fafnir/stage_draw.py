import panda3d.core as p3d
from OpenGL import GL as gl


class StageDraw:
    def __init__(self, data_manager):
        self.data = data_manager
        self.is_enabled = False

        self.callback_np = None
        self.camera = None
        self.root_np = None

        self.shader_resolve = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex='shaders/fsq.vert',
            fragment='shaders/resolve_intersections.frag'
        )

    def cb_resolve_intersections(self, cbdata):
        instance_count = len(self.data.material_map.keys())
        gl.glDrawArraysInstanced(gl.GL_TRIANGLE_STRIP, 0, 4, instance_count)
        cbdata.upcall()

    def enable(self):
        if self.is_enabled:
            return
        self.is_enabled = True

        # Setup stage camera
        self.camera = base.make_camera(
            base.win,
            camName='Draw stage camera',
            mask=self.data.mask_draw,
            lens=base.cam.node().get_lens()
        )
        self.camera.node().get_display_region(0).set_sort(2)

        # Setup callback node
        cbnode = p3d.CallbackNode('Resolve ray intersections')
        cbnode.set_draw_callback(p3d.PythonCallbackObject(self.cb_resolve_intersections))
        self.callback_np = self.data.np_render.attach_new_node(cbnode)
        self.callback_np.set_bin('fixed', 45)
        self.callback_np.set_shader(self.shader_resolve)
        self.callback_np.set_shader_input('texture_intersections', self.data.texture_intersections)
        self.callback_np.set_shader_input('buffer_primitives', self.data.buffer_primitives)
        self.callback_np.set_shader_input('buffer_vertices', self.data.buffer_vertices)
        self.callback_np.set_shader_input('buffer_materials', self.data.buffer_materials)
        self.callback_np.set_depth_test(False)
        light_node_paths = self.data.np_scene_root.find_all_matches('**/+LightLensNode')
        for light_np in light_node_paths:
            self.callback_np.set_light(light_np)
        self.callback_np.hide(self.data.mask_rtt)

    def disable(self):
        if not self.is_enabled:
            return
        self.is_enabled = False

        if self.camera:
            self.camera.remove_node()
            self.camera = None

        if self.callback_np:
            self.callback_np.remove_node()
            self.callback_np = None

    def update(self):
        pass
