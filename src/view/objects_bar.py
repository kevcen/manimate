import sys
from intermediate.imobject import ICircle, IMarkupText, ISquare, IStar, ITriangle
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
        
        layout = QVBoxLayout()

        addTree = QPushButton("add tree")
        addTree.clicked.connect(self.add_tree)

        addCircle = QPushButton("add circle")
        addCircle.clicked.connect(lambda : state_handler.instant_add_object_to_curr(ICircle()))

        addSquare = QPushButton("add square")
        addSquare.clicked.connect(lambda : state_handler.instant_add_object_to_curr(ISquare()))
        
        addStar = QPushButton("add star")
        addStar.clicked.connect(lambda : state_handler.instant_add_object_to_curr(IStar()))

        addTriangle = QPushButton("add triangle")
        addTriangle.clicked.connect(lambda : state_handler.instant_add_object_to_curr(ITriangle()))

        addMarkupText = QPushButton("add text")
        addMarkupText.clicked.connect(lambda : state_handler.instant_add_object_to_curr(IMarkupText(
            """
            mergeHeaps :: Ord a => BinHeap a -> BinHeap a -> BinHeap a
            mergeHeaps h1 []
                = h1
            mergeHeaps [] h2
                = h2
            mergeHeaps h1@(t1 : h) h2@(t2 : h')
                | r < r'    = t1 : mergeHeaps h h2
                | r' < r    = t2 : mergeHeaps h1 h'
                | otherwise = mergeHeaps [combineTrees t1 t2] (mergeHeaps h h')
                where
                    r  = rank t1
                    r' = rank t2"""
        , state_handler=state_handler)))
        
        for w in (addTree, addCircle, addSquare, addTriangle, addStar, addMarkupText):
            layout.addWidget(w)
        
        self.setLayout(layout)

    def add_tree(self):
        node = INode(self.state_handler)
        node.show_node()
