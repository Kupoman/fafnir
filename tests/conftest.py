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


@pytest.fixture
def camera():
    nodepath = p3d.NodePath(p3d.Camera('camera', p3d.PerspectiveLens()))
    return nodepath


@pytest.fixture
def half_screen_quad():
    vdata = p3d.GeomVertexData(
        'half_screen_quad',
        p3d.GeomVertexFormat.get_v3n3c4t2(),
        p3d.Geom.UHStatic
    )
    vdata.set_num_rows(4)

    vertex = p3d.GeomVertexWriter(vdata, 'vertex')
    normal = p3d.GeomVertexWriter(vdata, 'normal')
    color = p3d.GeomVertexWriter(vdata, 'color')
    texcoord = p3d.GeomVertexWriter(vdata, 'texcoord')

    scale = 10

    vertex.addData3f(-scale, 5, scale)
    normal.addData3f(0, 1, 0)
    color.addData4f(0.1, 0.2, 0.3, 1.0)
    texcoord.addData2f(0.0, 0.0)

    vertex.addData3f(0, 5, scale)
    normal.addData3f(0, 1, 0)
    color.addData4f(0.1, 0.2, 0.3, 1.0)
    texcoord.addData2f(0.0, 0.1)

    vertex.addData3f(0, 5, -scale)
    normal.addData3f(0, 1, 0)
    color.addData4f(0.1, 0.2, 0.3, 1.0)
    texcoord.addData2f(0.0, 0.2)

    vertex.addData3f(-scale, 5, -scale)
    normal.addData3f(0, 1, 0)
    color.addData4f(0.1, 0.2, 0.3, 1.0)
    texcoord.addData2f(0.0, 0.3)

    prim = p3d.GeomTriangles(p3d.Geom.UHStatic)
    prim.addVertices(2, 1, 0)
    prim.addVertices(0, 3, 2)

    geom = p3d.Geom(vdata)
    geom.addPrimitive(prim)

    node = p3d.GeomNode('gnode')
    node.addGeom(geom)

    nodepath = p3d.NodePath(node)
    return nodepath
