import os

import panda3d.core as p3d
from panda3d_render_pass import RenderPass


SHADER_DIR = os.path.join(os.path.dirname(__file__), 'shaders', '')


class ResolveIntersectionsPass(RenderPass):
    def __init__(self, name, graphics_context, texture_intersections, buffer_meshes):
        fb_props = p3d.FrameBufferProperties()
        fb_props.set_rgb_color(True)
        fb_props.set_rgba_bits(8, 8, 8, 0)
        super().__init__(
            name,
            **graphics_context,
            frame_buffer_properties=fb_props,
            clear_color=p3d.LColor(0.0, 0.0, 0.0, 0.0),
            shader=p3d.Shader.load(
                p3d.Shader.SL_GLSL,
                SHADER_DIR + 'fsq.vert',
                SHADER_DIR + 'resolve_intersections.frag'
            ),
        )

        self.buffer_materials = p3d.Texture()
        self._root.set_shader_input('texture_intersections', texture_intersections)
        self._root.set_shader_input('buffer_meshes', buffer_meshes.get_texture())
        self._root.set_shader_input('buffer_materials', self.buffer_materials)
        self._root.set_shader_input('instance_id', 1)
