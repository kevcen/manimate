import sys
from intermediate.ianimation import ICreate, IFadeIn
from intermediate.itext import Highlight, IMarkupText
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
    QComboBox,
    QTextEdit,
    QHBoxLayout,
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer
import models.mobject_helper as mh


class MarkupTextEdit(QTextEdit):
    def __init__(self, details_bar):
        super().__init__()
        self.details_bar = details_bar
        
    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.details_bar.changeMarkupTextHandler()

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

            match imobject:
                case INode():
                    self.addChildBtn.clicked.connect(imobject.spawn_child)
                    self.changeParentCb.addItem("None")
                    self.changeParentCb.addItems(filter(lambda name: name != mh.getName(imobject), map(mh.getName, mh.getImobjectsByClass(INode))))
                    for w in self.tree_widgets:
                        self.layout.addWidget(w)
                    
                    self.changeParentCb.setCurrentIndex(self.changeParentCb.findText(mh.getName(imobject.parent)) if imobject.parent is not None else 0)
                    self.changeNodeText.setText(mh.getCopy(imobject.label).text)
                case IMarkupText():
                    for w in self.text_widgets:
                        self.layout.addWidget(w)
                    
                    self.textEditLayout = QHBoxLayout()
                    for w in self.text_edits:
                        self.textEditLayout.addWidget(w)
                    self.layout.addLayout(self.textEditLayout)

                    self.changeMarkupText.setText(imobject.text)
            
            nameLbl.setText(mh.getName(imobject))
            self.introCb.setCurrentIndex(self.introCb.findText(imobject.introAnim.__class__.__name__[1:]) if imobject.introAnim is not None else 0)
        
        def clearItems():
            for i in reversed(range(self.layout.count())): 
                print(i)
                child = self.layout.itemAt(i).widget()
                if child is None:
                    child = self.layout.itemAt(i).layout()
                child.setParent(None)

            for i in reversed(range(self.textEditLayout.count())): 
                child = self.textEditLayout.itemAt(i).widget().setParent(None)
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

        self.changeNodeText = QLineEdit()
        self.changeNodeText.editingFinished.connect(self.changeNodeTextHandler)

        self.addChildBtn = QPushButton("add child")

        self.tree_widgets = (self.changeNodeText, self.changeParentCb, self.addChildBtn, )
    

        # Text widgets
        self.changeMarkupText = MarkupTextEdit(self)
        # self.changeMarkupText.focusOutEvent.connect(self.changeMarkupTextHandler)


        self.boldMarkupText = QPushButton("b")
        self.boldMarkupText.clicked.connect(lambda: self.highlightMarkupText(Highlight.BOLD))
        
        self.italicMarkupText = QPushButton("i")
        self.italicMarkupText.clicked.connect(lambda: self.highlightMarkupText(Highlight.ITALICS))
        
        self.underlineMarkupText = QPushButton("u")
        self.underlineMarkupText.clicked.connect(lambda: self.highlightMarkupText(Highlight.UNDERLINE))
        
        self.bigMarkupText = QPushButton("big")
        self.bigMarkupText.clicked.connect(lambda: self.highlightMarkupText(Highlight.BIG))
        
        self.colorMarkupText = QPushButton("red")
        self.colorMarkupText.clicked.connect(lambda: self.highlightMarkupText(Highlight.COLOR_CHANGE))

        self.text_edits = (self.boldMarkupText, self.italicMarkupText, self.underlineMarkupText, self.bigMarkupText, self.colorMarkupText)
        self.text_widgets = (self.changeMarkupText, )
        self.textEditLayout = QHBoxLayout()



        scene_handler.selectedMobjectChange.connect(selectedMobjectHandler)

        
        self.setLayout(self.layout)

    def highlightMarkupText(self, highlight):
        if self.selectedImobject is None:
            return

        cursor = self.changeMarkupText.textCursor()
        self.selectedImobject.handleBold(cursor.selectionStart(), cursor.selectionEnd(), highlight)


    
    def changeMarkupTextHandler(self):
        if self.selectedImobject is None:
            return
            
        text = self.changeMarkupText.plainText
        self.selectedImobject.changeText(text)

    def changeNodeTextHandler(self):
        text = self.changeNodeText.text
        self.selectedImobject.change_label_text(text)

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
            self.scene_handler.addCopy(imobject)
