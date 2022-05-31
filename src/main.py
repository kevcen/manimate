import sys
import signal
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QLineEdit
)

from PySide6.QtGui import QImage
from __feature__ import true_property
from file.reader import Reader
from models.fsm_model import FsmModel
from models.scene_model import SceneModel
import scene.manim_scene as manim_scene 
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer
from view.details_bar import DetailsBar
from view.objects_bar import ObjectsBar
from view.state_bar import StateWidget
from view.window import QTWindow


if __name__ == "__main__":
    # read_tokens = Reader("scene/manim_scene.py")
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    with tempconfig( {
        "input_file": Path("scene/manim_scene.py").absolute(), "disable_caching": True, "renderer": "opengl", "preview": True, "write_to_movie": False, "format": None
    }):

        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setVersion(3, 2)
        format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)
        renderer = OpenGLRenderer()
        window = QTWindow(app, renderer)
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

        scene_model = SceneModel(scene)
        fsm_model = FsmModel(scene_model)
        scene_model.setFsmModel(fsm_model)

        objects_bar = ObjectsBar(fsm_model)
        objects_bar.show()

        state_bar = StateWidget(scene_model, fsm_model)
        state_bar.show()


        details_bar = DetailsBar(scene_model, fsm_model)
        details_bar.show()


        with open("view/styles.qss", "r") as f:
            _style = f.read()
            for w in (objects_bar, details_bar, state_bar):
                w.setStyleSheet(_style)

        scene.render()


    sys.exit(app.exec())