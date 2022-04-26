import sys
from intermediate.ianimation import ICreate, IFadeIn
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
    QLineEdit,
    QComboBox
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer



class DetailsBar(QWidget):
    def __init__(self, scene_handler, state_handler):
        def selectedMobjectHandler(imobject):
            if imobject == self.selectedImobject:
                return #nothing happened 

            clearItems()

            classLbl.setText(imobject.__class__.__name__)
            addItems(imobject)

            self.selectedImobject = imobject

        def addItems(imobject):
            empty = imobject is None
            if empty:
                self.layout.addWidget(QLabel("nothing selected"))
            else: #fresh add
                for w in self.all_widgets:
                    self.layout.addWidget(w)

                if isinstance(imobject, INode):
                    self.addChildBtn.clicked.connect(imobject.spawn_child)
                    for w in self.tree_widgets:
                        self.layout.addWidget(w)
        
        def clearItems():
            for i in reversed(range(self.layout.count())): 
                self.layout.itemAt(i).widget().setParent(None)
                
            if isinstance(self.selectedImobject, INode):
                self.addChildBtn.clicked.disconnect(self.selectedImobject.spawn_child)


        super().__init__()

        self.scene_handler = scene_handler

        self.selectedImobject = None

        self.setWindowTitle(" ")

        self.geometry = QRect(1800, 250, 150, 600)

        self.layout = QVBoxLayout()

        classLbl = QLabel(self.selectedImobject.__class__.__name__)

        transformBtn = QPushButton("add transform")
        transformBtn.clicked.connect(state_handler.add_transform_to_curr)

        introCb = QComboBox()
        introCb.addItems(["Create", "FadeIn", "None"])
        introCb.currentIndexChanged.connect(self.introAnimationHandler)


        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)

        self.all_widgets = (classLbl, introCb, transformBtn,)

        # Tree widgets
        changeParentCb = QComboBox()

        self.addChildBtn = QPushButton("add child")

        self.tree_widgets = (changeParentCb, self.addChildBtn, )
    
        scene_handler.selectedMobjectChange.connect(selectedMobjectHandler)
        
        self.setLayout(self.layout)
        

    def introAnimationHandler(self, i):
        imobject = self.selectedImobject
        if imobject.introAnim is not None:
            imobject.addedState.animations.remove(imobject.introAnim)
        else:
            imobject.addedState.added.remove(imobject)

        self.scene_handler.remove(imobject)
        match i:
            case 0:
                imobject.introAnim = ICreate(imobject)
            case 1:
                imobject.introAnim = IFadeIn(imobject)
            case 2:
                imobject.introAnim = None

        if imobject.introAnim is not None:
            imobject.addedState.animations.append(imobject.introAnim)
            self.scene_handler.playCopy(imobject.introAnim, imobject.addedState)
        else:
            imobject.addedState.added.add(imobject)
            self.scene_handler.add(imobject)
