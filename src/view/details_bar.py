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
import models.mobject_helper as mh



class DetailsBar(QWidget):
    def __init__(self, scene_handler, state_handler):
        def selectedMobjectHandler(imobject):
            if imobject == self.selectedImobject:
                return #nothing happened 

            clearItems()

            addItems(imobject)

            self.selectedImobject = imobject

        def addItems(imobject):
            if imobject is None:
                self.layout.addWidget(QLabel("nothing selected"))
                return

            #fresh add
            for w in self.all_widgets:
                self.layout.addWidget(w)

            if isinstance(imobject, INode):
                self.addChildBtn.clicked.connect(imobject.spawn_child)
                self.changeParentCb.addItem("None")
                self.changeParentCb.addItems(filter(lambda name: name != mh.getName(imobject), map(mh.getName, mh.getImobjectsByClass(INode))))
                for w in self.tree_widgets:
                    self.layout.addWidget(w)
                
                self.changeParentCb.setCurrentIndex(self.changeParentCb.findText(mh.getName(imobject.parent)) if imobject.parent is not None else 0)

            
            nameLbl.setText(mh.getName(imobject))
            self.introCb.setCurrentIndex(self.introCb.findText(imobject.introAnim.__class__.__name__[1:]) if imobject.introAnim is not None else 0)
        
        def clearItems():
            for i in reversed(range(self.layout.count())): 
                self.layout.itemAt(i).widget().setParent(None)
                
            if isinstance(self.selectedImobject, INode):
                self.addChildBtn.clicked.disconnect(self.selectedImobject.spawn_child)
                self.changeParentCb.clear()



        super().__init__()

        self.scene_handler = scene_handler

        self.selectedImobject = None

        self.setWindowTitle(" ")

        self.geometry = QRect(1800, 250, 150, 600)

        self.layout = QVBoxLayout()

        nameLbl = QLabel(self.selectedImobject.__class__.__name__)

        # transformBtn = QPushButton("add transform")
        # transformBtn.clicked.connect(state_handler.add_transform_to_curr)

        self.introCb = QComboBox()
        self.introCb.addItems(["None", "Create", "FadeIn"])
        self.introCb.currentIndexChanged.connect(self.introAnimationHandler)

        removeBtn = QPushButton("remove mobject")
        removeBtn.clicked.connect(lambda: state_handler.instant_remove_obj_at_curr(self.selectedImobject))


        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)

        self.all_widgets = (nameLbl, self.introCb, removeBtn)

        # Tree widgets
        self.changeParentCb = QComboBox()
        self.changeParentCb.addItem("None")
        self.changeParentCb.currentIndexChanged.connect(self.changeParentHandler)

        self.addChildBtn = QPushButton("add child")

        self.tree_widgets = (self.changeParentCb, self.addChildBtn, )
    
        scene_handler.selectedMobjectChange.connect(selectedMobjectHandler)
        
        self.setLayout(self.layout)
    
    def changeParentHandler(self, i):
        if self.changeParentCb.count == 0 or not isinstance(self.selectedImobject, INode):
            return 

        imobj_name = self.changeParentCb.currentText
        imobj = mh.getImobjectByName(imobj_name) if imobj_name is not None else None

        self.selectedImobject.change_parent(imobj)


    def introAnimationHandler(self, i):
        if self.selectedImobject is None:
            return 

        imobject = self.selectedImobject
        if imobject.introAnim is not None:
            imobject.addedState.animations.remove(imobject.introAnim)
        else:
            imobject.addedState.added.remove(imobject)

        self.scene_handler.remove(imobject)
        match i:
            case 0:
                imobject.introAnim = None
            case 1:
                imobject.introAnim = ICreate(imobject)
            case 2:
                imobject.introAnim = IFadeIn(imobject)

        if imobject.introAnim is not None:
            imobject.addedState.animations.append(imobject.introAnim)
            self.scene_handler.playCopy(imobject.introAnim, imobject.addedState)
        else:
            imobject.addedState.added.add(imobject)
            self.scene_handler.add(imobject)
