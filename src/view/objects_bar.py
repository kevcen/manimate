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

from mobjects.tree import Node, Root



class ObjectsBar(QWidget):
    def __init__(self, state_handler, mobject_handler):
        super().__init__()

        self.setWindowTitle(" ")

        self.geometry = QRect(750, 250, 150, 600)
        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QVBoxLayout()

        # lineCmd = QLineEdit()

        button2 = QPushButton("add circle")
        button2.clicked.connect(lambda : state_handler.add_object_to_curr(Circle()))


        # button4 = QPushButton("add graph")
        # button4.clicked.connect(lambda : state_handler.add_object_to_curr(Graph([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)], layout='tree')))
        
        tree = Root(mobject_handler, text="n0")
        n1 = Node(mobject_handler, text="n1")
        n2 = Node(mobject_handler, text="n2")
        n3 = Node(mobject_handler, text="n3")
        n4 = Node(mobject_handler, text="n4")
        n5 = Node(mobject_handler, text="n5")
        tree.add_child(n1)
        tree.add_child(n2)
        n2.add_child(n3)
        n2.add_child(n4)
        n1.add_child(n5)

        tree.build(2,2)
        # g = tree.to_vgroup()


        button4 = QPushButton("add graph")
        button4.clicked.connect(lambda : tree.build_tree_to_scene(state_handler))

        button5 = QPushButton("add square")
        button5.clicked.connect(lambda : state_handler.add_object_to_curr(Square()))

        button3 = QPushButton("debug")
        button3.clicked.connect(lambda : self.debug())

        
        # self.manim.setFormat(format); # must be called before the widget or its parent window gets shown

        for w in (button2, button4, button5 ,button3):
            layout.addWidget(w)
        
        self.setLayout(layout)