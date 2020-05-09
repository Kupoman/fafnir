import sys

import fafnir

from direct.showbase.ShowBase import ShowBase
import panda3d.core as p3d
import pman.shim


p3d.load_prc_file(p3d.Filename.expand_from('$MAIN_DIR/settings.prc'))

p3d.load_prc_file_data(
    '',
    'win-size 1280 720\n'
    'show-frame-rate-meter true\n'
    'frame-rate-meter-milliseconds true\n'
    'textures-power-2 false\n'
    # 'gl-immutable-texture-storage true\n'
    # 'show-buffers #t\n'
    # 'notify-level-glgsg debug\n'
    # 'gl-debug #t\n'
    # 'gl-use-bindless-texture #t\n'
    'sync-video #f\n'
    'gl-version 3 3\n'
    # 'want-pstats true\n'
    # 'pstats-gpu-timing true\n'
)


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
        self.accept('escape', sys.exit)

        shader = p3d.Shader.load(
            p3d.Shader.SL_GLSL,
            vertex='phong.vert',
            fragment='phong.frag',
        )
        self.render.set_shader(shader)

        # Scene Setup
        scene = self.loader.load_model('happy.bam')
        self.happy = scene.find('happy')
        # scene.reparent_to(self.render)
        taskMgr.add(self.rotate_happy_task, 'Why is the room spinning?')

        fafnir.init(scene)

    def rotate_happy_task(self, task):
        hpr = self.happy.get_hpr()
        hpr.x += 50 * globalClock.get_dt()
        self.happy.set_hpr(hpr)
        return task.cont


GameApp().run()
