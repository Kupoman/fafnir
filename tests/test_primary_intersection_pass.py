import panda3d.core as p3d

from fafnir.geometry_pass import GeometryPass
from fafnir.primary_intersection_pass import PrimaryIntersectionPass

def print_image(view):
    for i, value in enumerate(view):
        end = ', '
        if i == 0:
            pass
        elif (i + 1) % 16 == 0:
            end = ',\n\n'
        elif (i + 1) % 4 == 0:
            end = ',\n'
        print(value, end=end)


def assert_image(graphics_context, gsg, texture, expected):
    graphics_context['engine'].extract_texture_data(texture, gsg)
    view = memoryview(texture.get_ram_image()).cast('f')
    print_image(view)
    assert list(view) == expected


def test_intersections(graphics_context, gsg, half_screen_quad, camera):
    geom_pass = GeometryPass(
        'test',
        graphics_context,
        scene=half_screen_quad,
        camera=camera
    )
    intersection_pass = PrimaryIntersectionPass(
        'test',
        graphics_context,
        geom_pass.mesh_buffer,
        camera
    )
    graphics_context['engine'].render_frame()

    texture = intersection_pass.outputs[0]

    # Check data type
    assert texture.get_component_type() == p3d.Texture.T_float
    assert texture.get_format() == p3d.Texture.F_rgba32

    # Check size
    assert texture.get_x_size() == graphics_context['window'].get_x_size()
    assert texture.get_y_size() == graphics_context['window'].get_y_size()
    assert texture.get_z_size() == 1

    assert_image(
        graphics_context,
        gsg,
        texture,
        [
            0.0, 0.3548608720302582, 0.5446581840515137, 2.0,
            0.0, 0.4218481481075287, 0.5446581840515137, 2.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,

            0.0, 0.39951905608177185, 0.4999999701976776, 2.0,
            0.0, 0.46650633215904236, 0.4999999701976776, 2.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,

            0.0, 0.4441772401332855, 0.45534178614616394, 2.0,
            0.0, 0.5111645460128784, 0.45534178614616394, 2.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
        ]
    )
