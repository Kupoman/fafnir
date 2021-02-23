import os

from OpenGL import GL as gl

import panda3d.core as p3d
from panda3d_render_pass import RenderPass


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')


class PrimaryIntersectionPass(RenderPass):
    def __init__(self, name, graphics_context, xfb, mesh_buffer, camera):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(True)
        fb_props.set_rgba_bits(32, 32, 32, 32)
        fb_props.set_depth_bits(24)
        fb_props.set_float_color(True)

        xfb_node = xfb.make_node()
        scene = p3d.NodePath(xfb_node)
        scene.set_shader_input('buffer_meshes', mesh_buffer.get_texture())

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
