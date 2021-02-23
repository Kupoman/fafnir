from .geometry_pass import GeometryPass
from .primary_intersection_pass import PrimaryIntersectionPass
from .depth_filter_pass import DepthFilterPass
from .resolve_intersections_pass import ResolveIntersectionsPass


class Renderer:
    def __init__(self, scene_root_np):
        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setCardSize(0, 0.40)
        base.bufferViewer.setLayout("vline")
        base.accept('f1', base.bufferViewer.toggleEnable)

        graphics_context = {
            'pipe': base.pipe,
            'window': base.win,
            'engine': base.win.get_engine()
        }

        geometry_pass = GeometryPass(
            'Fafnir Geometry Pass',
            graphics_context,
            scene=scene_root_np
        )
        intersection_pass = PrimaryIntersectionPass(
            'Fafnir Intersections Pass',
            graphics_context,
            geometry_pass.xfb,
            geometry_pass.mesh_buffer,
            base.camera
        )
        depth_filter_pass = DepthFilterPass(
            'Fafnir Depth Filter Pass',
            graphics_context,
            intersection_pass.outputs[0]
        )
        resolve_pass = ResolveIntersectionsPass(
            'Fafnir Resolve Intersections Pass',
            graphics_context,
            intersection_pass.outputs[0],
            geometry_pass.mesh_buffer,
            geometry_pass.material_buffer,
            geometry_pass.material_records,
            depth_filter_pass
        )

        final_pass = resolve_pass
        card = final_pass.buffer.getTextureCard()
        card.setTexture(final_pass.output)
        card.reparentTo(base.render2d)
