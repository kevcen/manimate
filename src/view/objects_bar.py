import sys
from model.state_handler import StateHandler
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot, QRect
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSlider,
    QLineEdit
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer



class ObjectsBar(QWidget):
    def __init__(self, state_handler):
        super().__init__()

        self.setWindowTitle(" ")

        self.geometry = QRect(750, 250, 150, 600)
        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QVBoxLayout()

        # lineCmd = QLineEdit()

        button2 = QPushButton("add circle")
        button2.clicked.connect(lambda : state_handler.add_object(Circle()))


        button4 = QPushButton("add graph")
        button4.clicked.connect(lambda : state_handler.add_object(Graph([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)])))

        button5 = QPushButton("add square")
        button5.clicked.connect(lambda : state_handler.add_object(Square()))

        button3 = QPushButton("debug")
        button3.clicked.connect(lambda : self.debug())

        
        # self.manim.setFormat(format); # must be called before the widget or its parent window gets shown

        for w in (button2, button4, button5 ,button3):
            layout.addWidget(w)
        
        self.setLayout(layout)