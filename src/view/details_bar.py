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
            addItems(imobject is None)

            self.selectedImobject = imobject

        def addItems(empty):
            if empty:
                self.layout.addWidget(QLabel("nothing selected"))
            else: #fresh add
                for w in self.all_widgets:
                    self.layout.addWidget(w)
        
        def clearItems():
            for i in reversed(range(self.layout.count())): 
                self.layout.itemAt(i).widget().setParent(None)


        super().__init__()

        self.selectedImobject = None

        self.setWindowTitle(" ")

        self.geometry = QRect(1800, 250, 150, 600)

        self.layout = QVBoxLayout()

        # lineCmd = QLineEdit()


        classLbl = QLabel(self.selectedImobject.__class__.__name__)

        transformBtn = QPushButton("add transform")
        transformBtn.clicked.connect(lambda : state_handler.add_transform_to_curr())

        introCb = QComboBox()
        introCb.addItems(["Create", "FadeIn", "None"])
        introCb.currentIndexChanged.connect(self.introAnimationHandler)


        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)

        self.all_widgets = (classLbl, transformBtn,)
    
        scene_handler.selectedMobjectChange.connect(selectedMobjectHandler)
        
        self.setLayout(self.layout)
        

    def introAnimationHandler(self, i):
        match i:
            case 0:
                #Create
                pass
            case 1:
                #FadeIn
                pass
            case 2:
                # instant add
                pass

