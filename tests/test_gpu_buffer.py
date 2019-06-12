import panda3d.core as p3d

from fafnir.gpu_buffer import GpuBufferRGBA32F


def test_constructor(gsg):
    count = 5
    buffer = GpuBufferRGBA32F('test', count, gsg)
    texture = buffer.get_texture()

    # Check name
    assert texture.name == 'test'

    # Check data type
    assert texture.get_component_type() == p3d.Texture.T_float
    assert texture.get_format() == p3d.Texture.F_rgba32

    # Check size
    assert texture.get_x_size() == count
    assert texture.get_y_size() == 1
    assert texture.get_z_size() == 1


def test_extract_data(gsg, engine):
    buffer = GpuBufferRGBA32F('test', 1, gsg)
    view = buffer.extract_data(engine)
    assert list(view) == [0, 0, 0, 0]


def test_buffer_id(gsg, engine):
    buffer0 = GpuBufferRGBA32F('zero', 1, gsg)
    buffer1 = GpuBufferRGBA32F('one', 1, gsg)
    engine.render_frame()

    assert buffer0.get_buffer_id() == 1
    assert buffer1.get_buffer_id() == 2
