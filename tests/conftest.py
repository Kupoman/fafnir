#pylint: disable=redefined-outer-name

import panda3d.core as p3d
import pytest


@pytest.fixture
def pipe():
    p3d.load_prc_file_data(
        '',
        'gl-version 3 3\n'
        'textures-power-2 false\n'
    )
    return p3d.GraphicsPipeSelection.get_global_ptr().make_default_pipe()


@pytest.fixture
def engine(pipe):
    return p3d.GraphicsEngine(pipe)


@pytest.fixture
def window(pipe, engine):
    fbprops = p3d.FrameBufferProperties()
    fbprops.set_rgba_bits(8, 8, 8, 0)
    fbprops.set_depth_bits(24)
    winprops = p3d.WindowProperties.size(4, 3)
    flags = p3d.GraphicsPipe.BF_refuse_window
    return engine.make_output(
        pipe,
        'window',
        0,
        fbprops,
        winprops,
        flags
    )


@pytest.fixture
def gsg(window):
    return window.get_gsg()


@pytest.fixture
def graphics_context(pipe, engine, window):
    return {
        'pipe': pipe,
        'engine': engine,
        'window': window,
    }
