import pytest

import panda3d.core as p3d

from fafnir.geometry_pass import GeometryPass


class Flag:
    def __init__(self):
        self.triggered = False


def test_xfb_activity(graphics_context):
    flags = {'active_during_render': False}
    geom_pass = None
    def xfb_check(callback_data):
        flags['active_during_render'] = geom_pass.xfb_active
        callback_data.upcall()
    scene = p3d.NodePath('scene')
    cb_node = p3d.CallbackNode('xfb_check')
    cb_node.set_draw_callback(p3d.PythonCallbackObject(xfb_check))
    scene.attach_new_node(cb_node)

    geom_pass = GeometryPass(
        'test',
        graphics_context,
        scene=scene
    )

    assert not geom_pass.xfb_active
    graphics_context['engine'].render_frame()
    assert not geom_pass.xfb_active

    assert flags['active_during_render']


def test_buffer_resize(graphics_context, half_screen_quad):
    geom_pass = GeometryPass(
        'test',
        graphics_context,
        scene=half_screen_quad,
    )

    graphics_context['engine'].render_frame()
    view = geom_pass.extract_mesh_cache()
    assert len(view) == 96


def test_scene(graphics_context, half_screen_quad, camera):
    geom_pass = GeometryPass(
        'test',
        graphics_context,
        scene=half_screen_quad,
        camera=camera
    )
    graphics_context['engine'].render_frame()
    view = list(geom_pass.extract_mesh_cache())
    assert view == pytest.approx([
        0, 5, -10, 1,
        0, 1, 0, 0,
        0.0, 0.2, 0, 0,
        0, 0, 0, 0,

        0, 5, 10, 1,
        0, 1, 0, 0,
        0.0, 0.1, 0, 0,
        0, 0, 0, 0,

        -10, 5, 10, 1,
        0, 1, 0, 0,
        0.0, 0.0, 0, 0,
        0, 0, 0, 0,

        -10, 5, 10, 1,
        0, 1, 0, 0,
        0.0, 0.0, 0, 0,
        0, 0, 0, 0,

        -10, 5, -10, 1,
        0, 1, 0, 0,
        0.0, 0.3, 0, 0,
        0, 0, 0, 0,

        0, 5, -10, 1,
        0, 1, 0, 0,
        0.0, 0.2, 0, 0,
        0, 0, 0, 0,

    ])


def test_scene_xform(graphics_context, half_screen_quad, camera):
    half_screen_quad.set_hpr(90, 0, 0)
    geom_pass = GeometryPass(
        'test',
        graphics_context,
        scene=half_screen_quad,
        camera=camera
    )
    graphics_context['engine'].render_frame()
    view = list(geom_pass.extract_mesh_cache())
    print(view)
    assert view == pytest.approx([
        -5, 0, -10, 1,
        -1, 0, 0, 0,
        0.0, 0.2, 0, 0,
        0, 0, 0, 0,

        -5, 0, 10, 1,
        -1, 0, 0, 0,
        0.0, 0.1, 0, 0,
        0, 0, 0, 0,

        -5, -10, 10, 1,
        -1, 0, 0, 0,
        0.0, 0.0, 0, 0,
        0, 0, 0, 0,

        -5, -10, 10, 1,
        -1, 0, 0, 0,
        0.0, 0.0, 0, 0,
        0, 0, 0, 0,

        -5, -10, -10, 1,
        -1, 0, 0, 0,
        0.0, 0.3, 0, 0,
        0, 0, 0, 0,

        -5, 0, -10, 1,
        -1, 0, 0, 0,
        0.0, 0.2, 0, 0,
        0, 0, 0, 0,

    ], abs=1.0e-5)
