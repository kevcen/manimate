import sys
import signal
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import (
    QApplication,
)

from models.fsm_model import FsmModel
from models.scene_model import SceneModel
import scene.manim_scene as manim_scene
from pathlib import Path
from view.details_bar import DetailsBar
from view.objects_bar import ObjectsBar
from view.state_bar import StateWidget
from view.window import QTWindow


windows = set()


def close_all():
    for window in windows:
        window.close()

    # sys.exit()


if __name__ == "__main__":
    # read_tokens = Reader("scene/manim_scene.py")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    with tempconfig(
        {
            "input_file": Path("scene/manim_scene.py").absolute(),
            "disable_caching": True,
            "renderer": "opengl",
            "preview": True,
            "write_to_movie": False,
            "format": None,
        }
    ):

        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 2)
        format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)
        renderer = OpenGLRenderer()
        window = QTWindow(app, renderer, close_all)
        windows.add(window._widget)
        renderer.window = window
        renderer.frame_buffer_object = window.ctx.detect_framebuffer()
        renderer.context = window.ctx
        renderer.context.enable(moderngl.BLEND)
        renderer.context.wireframe = config["enable_wireframe"]
        renderer.context.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
            moderngl.ONE,
            moderngl.ONE,
        )

        scene = manim_scene.Test(renderer)
        renderer.scene = scene

        scene_model = SceneModel(scene, renderer)
        fsm_model = FsmModel(scene_model)
        scene_model.set_fsm_model(fsm_model)

        objects_bar = ObjectsBar(fsm_model, close_all)
        objects_bar.show()

        state_bar = StateWidget(scene_model, fsm_model, close_all)
        state_bar.show()

        details_bar = DetailsBar(scene_model, fsm_model, close_all)
        details_bar.show()

        with open("view/styles.qss", "r") as f:
            _style = f.read()
            for w in (objects_bar, details_bar, state_bar):
                windows.add(w)
                w.setStyleSheet(_style)

        scene.render()

    sys.exit(app.exec())
