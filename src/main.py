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

from pathlib import Path
from os import path
from controllers.fsm_controller import FsmController
from controllers.scene_controller import SceneController
import scene.manim_scene as manim_scene
from view.details_bar import DetailsBar
from view.objects_bar import ObjectsBar
from view.state_bar import StateWidget
from view.preview_window import PreviewWindow

windows = set()

def close_all():
    for window in windows:
        window.close()

    # sys.exit()


def main():
    # read_tokens = Reader("scene/manim_scene.py")

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    this_dir, _ = path.split(__file__)
    with tempconfig(
        {
            "input_file": path.join(this_dir, "scene", "manim_scene.py"),
            "disable_caching": True,
            "renderer": "opengl",
            "preview": True,
            "write_to_movie": False,
            "format": None,
        }
    ):
        renderer = OpenGLRenderer()

        # Set the default surface format for the entire application
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 2)
        format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)

        scene = manim_scene.PreviewScene(renderer)
        renderer.scene = scene

        preview_window = PreviewWindow(app, renderer, close_all)
        windows.add(preview_window)

        scene_controller = SceneController(scene, renderer)
        fsm_controller = FsmController(scene_controller)
        scene_controller.set_fsm_controller(fsm_controller)

        objects_bar = ObjectsBar(fsm_controller, close_all)

        state_bar = StateWidget(scene_controller, fsm_controller, close_all)

        details_bar = DetailsBar(scene_controller, fsm_controller, close_all)

        for w in (preview_window, objects_bar, state_bar, details_bar):
            windows.add(w)
            w.show()

        print(path.join(this_dir, "view", "styles.qss"))
        with open(path.join(this_dir, "view", "styles.qss"), "r") as f:
            _style = f.read()
            for w in (objects_bar, details_bar, state_bar):
                w.setStyleSheet(_style)

    sys.exit(app.exec())



if __name__ == "__main__":
    main()