import os

import panda3d.core as p3d

from .data_manager import DataManager
from .stage_gather import StageGather
from .stage_draw import StageDraw


class Renderer:
    def __init__(self, scene_root_np, render_np):
        # Setup model path so shaders can be loaded
        fafnir_dir = os.path.dirname(os.path.realpath(__file__))
        p3d.get_model_path().prepend_directory(fafnir_dir)

        self.data = DataManager(scene_root_np, render_np)

        # Setup stages
        self.stages = [
            StageGather(self.data),
            StageDraw(self.data),
        ]
        self.enable_stages(2)
        self.enable_debug_bindings()

        # Hook into task manager
        def task_update(task):
            self.update()
            return task.cont
        taskMgr.add(task_update, 'Fafnir update')

    def enable_debug_bindings(self):
        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setCardSize(0, 0.40)
        base.bufferViewer.setLayout("vline")
        base.accept('f1', base.bufferViewer.toggleEnable)

        def debug_dump():
            print(base.render.ls())
        base.accept('f2', debug_dump)

        for i in range(len(self.stages) + 1):
            base.accept(str(i), self.enable_stages, [i])

    def enable_stages(self, final_stage):
        base.cam.node().set_active(final_stage == 0)

        for stage in self.stages:
            stage.disable()

        for i in range(final_stage):
            self.stages[i].enable()
            self.stages[i].update()

    def update(self):
        self.data.update()
        for stage in self.stages:
            if stage.is_enabled:
                stage.update()
