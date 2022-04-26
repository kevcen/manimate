import sys
from intermediate.imobject import ICircle, ISquare
from intermediate.itree import INode
from models.fsm_model import StateHandler
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

        self.state_handler = state_handler

        self.setWindowTitle(" ")

        self.geometry = QRect(750, 250, 150, 600)
        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QVBoxLayout()

        # lineCmd = QLineEdit()

        button2 = QPushButton("add circle")
        button2.clicked.connect(lambda : state_handler.instant_add_object_to_curr(ICircle()))

        button4 = QPushButton("add tree")
        button4.clicked.connect(self.add_tree)

        button5 = QPushButton("add square")
        button5.clicked.connect(lambda : state_handler.instant_add_object_to_curr(ISquare()))

        button3 = QPushButton("debug")
        button3.clicked.connect(lambda : self.debug())

        
        # self.manim.setFormat(format); # must be called before the widget or its parent window gets shown

        for w in (button2, button4, button5 ,button3):
            layout.addWidget(w)
        
        self.setLayout(layout)

    def add_tree(self):
        node = INode(self.state_handler)
        node.show_node()
