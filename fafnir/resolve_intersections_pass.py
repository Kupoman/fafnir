import os

import panda3d.core as p3d
from OpenGL import GL as gl

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

    def _make_draw_path(self):
        def draw_callback(callback_data):
            for i, record in enumerate(self.material_records):
                gl.glUniform1i(0, i)
                gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
            callback_data.upcall()

        cb_node = p3d.CallbackNode('Intersection Draw Callback')
        cb_node.draw_callback = p3d.PythonCallbackObject(draw_callback)
        cb_node_path = p3d.NodePath(cb_node)
        cb_node_path.set_shader_input('instance_id', 3)
        return cb_node_path
