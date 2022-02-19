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
from __feature__ import true_property
from fsm.state_handler import StateHandler
import scene.manim_scene as manim_scene 
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer
from scene.scene_handler import SceneHandler
from view.objects_bar import ObjectsBar

from view.state_bar import StateWidget
from view.window import QTWindow


states = [] #list of dictionary, mobject -> state 






if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    with tempconfig( {
        "input_file": Path("scene/manim_scene.py").absolute(), "renderer": "opengl", "preview": True, "write_to_movie": False, "format": None
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

        scene_handler = SceneHandler(scene)
        state_handler = StateHandler(scene_handler)

        widget = ObjectsBar(state_handler)
        widget.show()

        state_bar = StateWidget(scene_handler, state_handler)
        state_bar.show()

        # window._widget.hide()
        # window._widget.show()

        scene.render()

    sys.exit(app.exec())