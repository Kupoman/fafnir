import panda3d.core as p3d

from fafnir.ray_pass import RayPass

def print_image(view):
    for i, value in enumerate(view):
        end = ', '
        if i == 0:
            end = end
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


def test_screen_rays(graphics_context, gsg):
    ray_pass = RayPass('test', graphics_context)
    graphics_context['engine'].render_frame()

    texture = ray_pass.outputs[0]

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
        ray_pass.outputs[0],
        [
            -0.17863279581069946, 1.0, -0.2009618878364563, 1.0,
            -0.17863279581069946, 1.0, -0.0669872984290123, 1.0,
            -0.17863279581069946, 1.0, 0.0669872984290123, 1.0,
            -0.17863279581069946, 1.0, 0.2009618878364563, 1.0,

            0.0, 1.0, -0.2009618878364563, 1.0,
            0.0, 1.0, -0.0669872984290123, 1.0,
            7.985507366470301e-09, 1.0, 0.0669872984290123, 1.0,
            0.0, 1.0, 0.2009618878364563, 1.0,

            0.17863281071186066, 1.0, -0.2009618878364563, 1.0,
            0.17863281071186066, 1.0, -0.0669872984290123, 1.0,
            0.17863281071186066, 1.0, 0.0669872984290123, 1.0,
            0.17863281071186066, 1.0, 0.2009618878364563, 1.0,
        ]
    )

    assert_image(
        graphics_context,
        gsg,
        ray_pass.outputs[1],
        [
            -0.1725059300661087, 0.9657012820243835, -0.19406916201114655, 1.0,
            -0.1754681020975113, 0.9822837114334106, -0.06580053269863129, 1.0,
            -0.1754681020975113, 0.9822837114334106, 0.06580053269863129, 1.0,
            -0.1725059300661087, 0.9657012820243835, 0.19406916201114655, 1.0,

            0.0, 0.980398952960968, -0.19702284038066864, 1.0,
            0.0, 0.9977639317512512, -0.06683751195669174, 1.0,
            7.96765142752065e-09, 0.9977639317512512, 0.06683751195669174, 1.0,
            0.0, 0.980398952960968, 0.19702284038066864, 1.0,

            0.1725059449672699, 0.9657012820243835, -0.19406916201114655, 1.0,
            0.1754681020975113, 0.9822837114334106, -0.06580053269863129, 1.0,
            0.17546811699867249, 0.9822837114334106, 0.06580053269863129, 1.0,
            0.1725059449672699, 0.9657012820243835, 0.19406916201114655, 1.0,
        ]
    )
