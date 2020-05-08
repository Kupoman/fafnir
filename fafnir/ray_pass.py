import os

import panda3d.core as p3d
from panda3d_render_pass import RenderPass


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')


class RayPass(RenderPass):
    def __init__(self, name, graphics_context):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(True)
        fb_props.set_aux_rgba(1)
        fb_props.set_rgba_bits(32, 32, 32, 32)
        fb_props.set_float_color(True)
        super().__init__(
            name,
            **graphics_context,
            frame_buffer_properties=fb_props,
            clear_color=p3d.LColor(0.0, 0.0, 0.0, 0.0),
            shader=p3d.Shader.load(
                p3d.Shader.SL_GLSL,
                SHADER_DIR + 'generate_primary_rays.vert',
                SHADER_DIR + 'generate_primary_rays.frag'
            ),
        )
