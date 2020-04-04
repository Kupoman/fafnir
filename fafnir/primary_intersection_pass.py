import os

from OpenGL import GL as gl

import panda3d.core as p3d
from panda3d_render_pass import RenderPass


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')


class PrimaryIntersectionPass(RenderPass):
    def __init__(self, name, graphics_context, mesh_buffer, camera):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(True)
        fb_props.set_rgba_bits(32, 32, 32, 32)
        fb_props.set_depth_bits(24)
        fb_props.set_float_color(True)

        scene = self._make_xfb_path(mesh_buffer)

        super().__init__(
            name,
            **graphics_context,
            frame_buffer_properties=fb_props,
            clear_color=p3d.LColor(0.0, 0.0, 0.0, 0.0),
            scene=scene,
            camera=camera,
            shader=p3d.Shader.load(
                p3d.Shader.SL_GLSL,
                SHADER_DIR + 'generate_primary_intersections.vert',
                SHADER_DIR + 'generate_primary_intersections.frag'
            ),
        )

    def _make_xfb_path(self, buffer):
        def draw_callback(callback_data):
            gl.glDrawTransformFeedback(gl.GL_TRIANGLES, 0)
            callback_data.upcall()


        cb_node = p3d.CallbackNode('XFB Draw Callback')
        cb_node.draw_callback = p3d.PythonCallbackObject(draw_callback)
        cb_node_path = p3d.NodePath(cb_node)
        cb_node_path.set_shader_input('buffer_meshes', buffer.get_texture())
        return cb_node_path
