import os

import panda3d.core as p3d
from panda3d_render_pass import RenderPass


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')


class DepthFilterPass(RenderPass):
    def __init__(self, name, graphics_context, texture_intersections):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_depth_bits(24)
        fb_props.set_float_depth(False)
        fb_props.set_rgba_bits(0, 0, 0, 0)
        super().__init__(
            name,
            **graphics_context,
            frame_buffer_properties=fb_props,
            clear_color=p3d.LColor(0.0, 0.0, 0.0, 0.0),
            shader=p3d.Shader.load(
                p3d.Shader.SL_GLSL,
                SHADER_DIR + 'depth_filter.vert',
                SHADER_DIR + 'depth_filter.frag'
            ),
        )
        self.buffer.set_clear_depth(0.0)
        self._root.set_shader_input('texture_intersections', texture_intersections)
        self._root.set_attrib(p3d.DepthTestAttrib.make(p3d.RenderAttrib.MAlways))
