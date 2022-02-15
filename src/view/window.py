import sys
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
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer


class ManimWidget(QWidget):
    def __init__(self, scene):
        super().__init__()

        self.setWindowTitle("Widgets App")


        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QVBoxLayout()

        # lineCmd = QLineEdit()

        button2 = QPushButton("add a circle")
        button2.clicked.connect(lambda : scene.add(Circle()))



        button4 = QPushButton("fade in a circle")
        button4.clicked.connect(lambda : scene.play(FadeIn(Circle())))

        button5 = QPushButton("create a circle")
        button5.clicked.connect(lambda : scene.play(Create(Square())))

        button3 = QPushButton("debug")
        button3.clicked.connect(lambda : self.debug())

        
        # self.manim.setFormat(format); # must be called before the widget or its parent window gets shown

        for w in (button2, button4, button5 ,button3):
            layout.addWidget(w)
        
        self.setLayout(layout)



class QTWindow(PySideWindow):
    def __init__(self, app, renderer) -> None:
        super().__init__()

        self.title = f"Manimate"
        # self.size = size
        self.renderer = renderer

        mglw.activate_context(window=self)
        self.timer = Timer()
        self.config = mglw.WindowConfig(ctx=self.ctx, wnd=self, timer=self.timer)
        self.timer.start()

        self.swap_buffers()

    
    # Delegate event handling to scene.
    def mouse_move_event(self, event):
        super().mouse_move_event(event)
        x, y = event.x(), event.y()
        dx, dy = self._calc_mouse_delta(x, y)
        point = self.renderer.pixel_coords_to_space_coords(x, y)
        d_point = self.renderer.pixel_coords_to_space_coords(dx, dy, relative=True)
        self.renderer.scene.mouse_move_event(point, d_point)

    def key_pressed_event(self, event):
        key = event.key()
        self.renderer.pressed_keys.add(key)
        super().key_pressed_event(event)
        self.renderer.scene.on_key_press(key, None)

    def key_release_event(self, event):
        key = event.key()
        if key in self.renderer.pressed_keys:
            self.renderer.pressed_keys.remove(key)
        super().key_release_event(event)
        self.renderer.scene.on_key_release(key, None)

    # def swap_buffers(self):
    #     # self.widget.update()
    #     pass
