import sys
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



class DetailsBar(QWidget):
    def __init__(self, scene_handler, state_handler):
        def selectedMobjectHandler(mobject):
            clearItems()
            addItems(mobject is None)

        def addItems(empty):
            if empty:
                self.layout.addWidget(self.emptyLabel)
            else:
                for w in self.all_widgets:
                    self.layout.addWidget(w)
        
        def clearItems():
            for w in self.all_widgets:
                w.setParent(None)
            self.emptyLabel.setParent(None)
            


        super().__init__()

        self.setWindowTitle(" ")

        self.geometry = QRect(1800, 250, 150, 600)

        self.layout = QVBoxLayout()

        # lineCmd = QLineEdit()

        button2 = QPushButton("add transform")
        button2.clicked.connect(lambda : state_handler.add_transform_to_curr())

        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)

        self.all_widgets = (button2,)
        # button4 = QPushButton("add graph")
        # button4.clicked.connect(lambda : state_handler.add_object(Graph([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)])))

        # button5 = QPushButton("add square")
        # button5.clicked.connect(lambda : state_handler.add_object(Square()))


        scene_handler.selectedMobjectChange.connect(selectedMobjectHandler)
        
        # self.manim.setFormat(format); # must be called before the widget or its parent window gets shown


        self.setLayout(self.layout)
        
