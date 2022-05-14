import sys
from intermediate.ianimation import ICreate, IFadeIn
from intermediate.itext import Highlight, IMarkupText, IMathTex
from intermediate.itree import INode
from models.fsm_model import StateHandler
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat, QIntValidator, QDoubleValidator
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
        super().__init__()

        self.scene_handler = scene_handler
        self.state_handler = state_handler

        self.selectedImobject = None

        self.setWindowTitle(" ")

        self.geometry = QRect(1800, 250, 150, 600)

        self.layout = QVBoxLayout()

        self.nameLbl = QLabel(self.selectedImobject.__class__.__name__)

        # transformBtn = QPushButton("add transform")
        # transformBtn.clicked.connect(state_handler.add_transform_to_curr)


        self.animationRunTime = QLineEdit()
        validator = QDoubleValidator()
        validator.bottom = 0
        self.animationRunTime.setValidator(validator)
        print("run time is " + str(state_handler.curr.run_time))
        self.animationRunTime.editingFinished.connect(self.changeAnimationRunTimeHandler)

        self.introCb = QComboBox()
        self.introCb.addItems(["None", "Create", "FadeIn"])
        self.introCb.currentIndexChanged.connect(self.introAnimationHandler)

        removeBtn = QPushButton("remove mobject")
        removeBtn.clicked.connect(lambda: state_handler.instant_remove_obj_at_curr(self.selectedImobject))
        
        self.stateLabel = QLabel(f"State {state_handler.curr.idx}")
        self.layout.addWidget(self.stateLabel)
        self.animationRunTime.setText(str(state_handler.curr.run_time))
        self.layout.addWidget(self.animationRunTime)
        self.layout.addStretch()
        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)
        self.layout.addStretch()
        

        self.all_widgets = (self.nameLbl, self.introCb, removeBtn)

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

        self.currIdx = -1



        scene_handler.selectedMobjectChange.connect(lambda mob: self.refresh(mob))
        state_handler.stateChange.connect(lambda: self.refresh())

        
        self.setLayout(self.layout)

    def refresh(self, imobject=None):
        print('REFRESH')
        if imobject == self.selectedImobject and self.currIdx == self.state_handler.curr.idx:
            return #nothing happened 
        if imobject is None:
            imobject = self.selectedImobject
        self.currIdx = self.state_handler.curr.idx
        self.clearItems()
        self.addItems(imobject)

        self.selectedImobject = imobject


    def addItems(self, imobject):
        # self.layout.insertWidget(self.layout.count()-1, QLabel(f"State {self.state_handler.curr.idx}"))
        # self.animationRunTime.setText(str(self.state_handler.curr.run_time))
        # self.layout.insertWidget(self.layout.count()-1, self.animationRunTime)
        # self.layout.addStretch()

        self.stateLabel.setText(f"State {self.state_handler.curr.idx}")
        self.animationRunTime.setText(str(self.state_handler.curr.run_time))
        if imobject is None:
            self.layout.insertWidget(self.layout.count()-1, QLabel("nothing selected"))
            return

        #fresh add
        for w in self.all_widgets:
            self.layout.insertWidget(self.layout.count()-1, w)

        match imobject:
            case INode():
                self.addChildBtn.clicked.connect(imobject.spawn_child)
                self.changeParentCb.addItem("None")
                self.changeParentCb.addItems(filter(lambda name: name != mh.getName(imobject), map(mh.getName, mh.getImobjectsByClass(INode))))
                for w in self.tree_widgets:
                    self.layout.insertWidget(self.layout.count()-1, w)
                
                self.changeParentCb.setCurrentIndex(self.changeParentCb.findText(mh.getName(imobject.parent)) if imobject.parent is not None else 0)
                self.changeNodeText.setText(mh.getCopy(imobject.label).text)
            case IMarkupText() | IMathTex():
                for w in self.text_widgets:
                    self.layout.insertWidget(self.layout.count()-1, w)
                self.changeMarkupText.setText(imobject.text)

                if isinstance(imobject, IMarkupText):
                    self.textEditLayout = QHBoxLayout()
                    for w in self.text_edits:
                        self.textEditLayout.addWidget(w)
                    self.layout.insertLayout(self.layout.count()-1, self.textEditLayout)

        
        self.nameLbl.setText(mh.getName(imobject))
        self.introCb.setCurrentIndex(self.introCb.findText(imobject.introAnim.__class__.__name__[1:]) if imobject.introAnim is not None else 0)


        # self.layout.addStretch()
    
    def clearItems(self):
        for i in range(self.layout.count()-2, 2, -1): 
            print(i)
            child = self.layout.itemAt(i).widget()
            if child is None:
                child = self.layout.itemAt(i).layout()
            print(child.__class__.__name__)
            # if child is None:
            #     continue
            child.setParent(None)

        for i in reversed(range(self.textEditLayout.count())): 
            child = self.textEditLayout.itemAt(i).widget().setParent(None)
        if isinstance(self.selectedImobject, INode):
            self.addChildBtn.clicked.disconnect(self.selectedImobject.spawn_child)
            self.changeParentCb.clear()

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

    def changeAnimationRunTimeHandler(self):
        time = float(self.animationRunTime.text)
        self.state_handler.curr.run_time = time

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
