import sys
from intermediate.imobject import ICircle, ISquare, IStar, ITriangle
from intermediate.itext import IMarkupText, IMathTex
from intermediate.itree import INode
from models.fsm_model import FsmModel
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
    QLineEdit,
    QTabWidget,
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer




class ObjectsBar(QTabWidget):
    def __init__(self, fsm_model):
        super().__init__()

        self.fsm_model = fsm_model

        self.setWindowTitle(" ")

        self.geometry = QRect(300, 250, 300, 600)

        self.addTab(self.file_tab(), "File")
        self.addTab(self.object_tab(), "Add Objects")
        self.addTab(self.animation_tab(), "Animation")

        self.tabPosition = QTabWidget.West
        self.setCurrentIndex(1)

    def file_tab(self): 
        tab = QWidget()
        layout = QVBoxLayout()

        exit = QPushButton("Exit")
        save = QPushButton("Save As Python Script")
        export = QPushButton("Export As MP4")
        importBtn = QPushButton("Import Python Script As Frame")
        # addTree.clicked.connect(self.add_tree)

        for w in (save, export, importBtn, export, exit):
            layout.addWidget(w)

        tab.setLayout(layout)
        return tab

    def animation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        addFrame = QPushButton("New Frame (+)")
        delFrame = QPushButton("Delete Current Frame (-)")

        for w in (addFrame, delFrame):
            layout.addWidget(w)

        tab.setLayout(layout)
        return tab


    def object_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        addTree = QPushButton("add tree")
        addTree.clicked.connect(self.add_tree)

        addCircle = QPushButton("add circle")
        addCircle.clicked.connect(lambda : self.fsm_model.instant_add_object_to_curr(ICircle()))

        addSquare = QPushButton("add square")
        addSquare.clicked.connect(lambda : self.fsm_model.instant_add_object_to_curr(ISquare()))
        
        addStar = QPushButton("add star")
        addStar.clicked.connect(lambda : self.fsm_model.instant_add_object_to_curr(IStar()))

        addTriangle = QPushButton("add triangle")
        addTriangle.clicked.connect(lambda : self.fsm_model.instant_add_object_to_curr(ITriangle()))

        addMarkupText = QPushButton("add text")
        addMarkupText.clicked.connect(lambda : self.fsm_model.instant_add_object_to_curr(IMarkupText(
            """click to add text"""
            # mergeHeaps h1@(t1 : h) h2@(t2 : h')
            #     | r < r'    = t1 : mergeHeaps h h2
            #     | r' < r    = t2 : mergeHeaps h1 h'
            #     | otherwise = mergeHeaps [combineTrees t1 t2] (mergeHeaps h h')
            #     where
            #         r  = rank t1
            #         r' = rank t2"""
        , fsm_model=self.fsm_model)))

        addMathTex = QPushButton("add latex")
        addMathTex.clicked.connect(lambda : self.fsm_model.instant_add_object_to_curr(IMathTex(r"\xrightarrow{x^6y^8}", fsm_model=fsm_model)))
        
        for w in (addTree, addCircle, addSquare, addTriangle, addStar, addMarkupText, addMathTex):
            layout.addWidget(w)
        
        tab.setLayout(layout)
        return tab

    def add_tree(self):
        node = INode(self.fsm_model)
        node.show_node()
