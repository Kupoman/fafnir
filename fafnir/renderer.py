from .geometry_pass import GeometryPass
from .primary_intersection_pass import PrimaryIntersectionPass
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
            'fafnir',
            graphics_context,
            scene=scene_root_np
        )
        intersection_pass = PrimaryIntersectionPass(
            'fafnir',
            graphics_context,
            geometry_pass.mesh_buffer,
            base.camera
        )
        resolve_pass = ResolveIntersectionsPass(
            'fafnir',
            graphics_context,
            intersection_pass.outputs[0],
            geometry_pass.mesh_buffer
        )

        final_pass = resolve_pass
        card = final_pass.buffer.getTextureCard()
        card.setTexture(final_pass.output)
        card.reparentTo(base.render2d)
