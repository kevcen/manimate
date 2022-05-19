import sys
from intermediate.ianimation import ICreate, IFadeIn
from intermediate.itext import Highlight, IMarkupText, IMathTex
from intermediate.itree import INode
from models.fsm_model import FsmModel
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

TOP_WIDGETS_NUM = 4
class DetailsBar(QWidget):
    def __init__(self, scene_model, fsm_model):
        super().__init__()

        self.scene_model = scene_model
        self.fsm_model = fsm_model

        self.selectedImobject = None

        self.setWindowTitle(" ")

        self.geometry = QRect(1500, 250, 150, 600)

        self.layout = QVBoxLayout()

        self.animationRunTime = QLineEdit()
        doubleValidator = QDoubleValidator()
        doubleValidator.bottom = 0
        self.animationRunTime.setValidator(doubleValidator)
        print("run time is " + str(fsm_model.curr.run_time))
        self.animationRunTime.editingFinished.connect(self.changeAnimationRunTimeHandler)
        self.stateLabel = QLabel(f"State {fsm_model.curr.idx}")

        self.loopCb = QComboBox()
        self.loopCb.addItem("None")
        self.loopCb.addItems([f"State {n}" for n in range(1, fsm_model.end.idx)])
        self.loopCb.currentIndexChanged.connect(self.loopStateChangeHandler)

        self.loopTimes = QLineEdit()
        intValidator = QIntValidator()
        intValidator.bottom = 0
        self.loopTimes.setValidator(intValidator)
        self.loopTimes.editingFinished.connect(self.changeLoopTimes)

        self.layout.addWidget(self.stateLabel)
        self.animationRunTime.setText(str(fsm_model.curr.run_time))
        self.layout.addWidget(self.animationRunTime)
        self.layout.addWidget(self.loopCb)
        self.layout.addWidget(self.loopTimes)
        self.layout.addStretch()
        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)
        self.layout.addStretch()

        self.nameLbl = QLabel(self.selectedImobject.__class__.__name__)
        
        self.introCb = QComboBox()
        self.introCb.addItems(["None", "Create", "FadeIn"])
        self.introCb.currentIndexChanged.connect(self.introAnimationHandler)

        removeBtn = QPushButton("remove mobject")
        removeBtn.clicked.connect(lambda: fsm_model.instant_remove_obj_at_curr(self.selectedImobject))
        

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



        scene_model.selectedMobjectChange.connect(lambda mob: self.refresh(mob))
        fsm_model.stateChange.connect(lambda: self.refresh())

        
        self.setLayout(self.layout)

    def refresh(self, imobject=None):
        print('REFRESH')
        if imobject == self.selectedImobject and self.currIdx == self.fsm_model.curr.idx:
            return #nothing happened 
        if imobject is None:
            imobject = self.selectedImobject
        self.currIdx = self.fsm_model.curr.idx
        self.clearItems()
        self.selectedImobject = imobject
        self.addItems(imobject)



    def addItems(self, imobject):
        # self.layout.insertWidget(self.layout.count()-1, QLabel(f"State {self.fsm_model.curr.idx}"))
        # self.animationRunTime.setText(str(self.fsm_model.curr.run_time))
        # self.layout.insertWidget(self.layout.count()-1, self.animationRunTime)
        # self.layout.addStretch()

        self.stateLabel.setText(f"State {self.fsm_model.curr.idx}")
        self.animationRunTime.setText(str(self.fsm_model.curr.run_time))
        self.loopCb.addItem("None")
        self.loopCb.addItems([f"State {n}" for n in range(1, self.fsm_model.end.idx)])
        self.loopCb.setCurrentIndex(self.loopCb.findText(f"State {self.fsm_model.curr.loop[0]}") if self.fsm_model.curr.loop is not None else 0)
        self.loopCb.blockSignals(False)
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
                
                print("SET PARENT", mh.getName(imobject.parent) if imobject.parent is not None else "None")
                self.changeParentCb.setCurrentIndex(self.changeParentCb.findText(mh.getName(imobject.parent)) if imobject.parent is not None else 0)
                self.changeParentCb.blockSignals(False)
                self.changeNodeText.blockSignals(True)
                self.changeNodeText.setText(mh.getCopy(imobject.label).text)
                self.changeNodeText.blockSignals(False)
            case IMarkupText() | IMathTex():
                for w in self.text_widgets:
                    self.layout.insertWidget(self.layout.count()-1, w)
                    
                self.changeMarkupText.blockSignals(True)
                self.changeMarkupText.setText(imobject.text)
                self.changeMarkupText.blockSignals(True)
                

                if isinstance(imobject, IMarkupText):
                    self.textEditLayout = QHBoxLayout()
                    for w in self.text_edits:
                        self.textEditLayout.addWidget(w)
                    self.layout.insertLayout(self.layout.count()-1, self.textEditLayout)

        
        self.nameLbl.setText(mh.getName(imobject))
        # print("REFRESHED INTRO", imobject.introAnim.__class__.__name__ if imobject.introAnim is not None else 'None')
        self.introCb.blockSignals(True)
        self.introCb.setCurrentIndex(self.introCb.findText(imobject.introAnim.__class__.__name__[1:]) if imobject.introAnim is not None else 0)
        self.introCb.blockSignals(False)


        # self.layout.addStretch()
    
    def clearItems(self):
        for i in range(self.layout.count()-2, TOP_WIDGETS_NUM, -1): 
            child = self.layout.itemAt(i).widget()
            if child is None:
                child = self.layout.itemAt(i).layout()
            if child is not None:
                child.setParent(None)

        for i in reversed(range(self.textEditLayout.count())): 
            child = self.textEditLayout.itemAt(i).widget().setParent(None)

        if isinstance(self.selectedImobject, INode):
            self.addChildBtn.clicked.disconnect(self.selectedImobject.spawn_child)
            self.changeParentCb.blockSignals(True)
            self.changeParentCb.clear()

        self.loopCb.blockSignals(True)
        self.loopCb.clear()

    def highlightMarkupText(self, highlight):
        if self.selectedImobject is None:
            return

        cursor = self.changeMarkupText.textCursor()
        self.selectedImobject.handleBold(cursor.selectionStart(), cursor.selectionEnd(), highlight)

    def loopStateChangeHandler(self, i):
        if self.changeParentCb.count == 0 or not self.loopCb.currentText:
            return 

        print('CHANGE LOOP TIMES', self.loopCb.currentText)
        if self.loopCb.currentText == "None":
            self.fsm_model.curr.loop = None
        else:
            state_num = int(self.loopCb.currentText[6:])
            if not self.loopTimes.text:
                self.loopTimes.setText('1')

            self.fsm_model.curr.loop = (state_num, 1)
            self.fsm_model.curr.loopCnt = 1

    def changeLoopTimes(self):
        num = int(self.loopTimes.text)
        self.fsm_model.curr.loopCnt = num

    def changeMarkupTextHandler(self):
        if self.selectedImobject is None:
            return
        
        text = self.changeMarkupText.plainText
        self.selectedImobject.changeText(text)
        self.selectedImobject.editedAt = self.fsm_model.curr.idx 

    def changeNodeTextHandler(self):
        text = self.changeNodeText.text
        self.selectedImobject.change_label_text(text)
        self.selectedImobject.editedAt = self.fsm_model.curr.idx 

    def changeAnimationRunTimeHandler(self):
        time = float(self.animationRunTime.text)
        self.fsm_model.curr.run_time = time

    def changeParentHandler(self, i):
        if self.changeParentCb.count == 0 or not isinstance(self.selectedImobject, INode):
            return 

        # print("CHANGE PARENT")
        imobj_name = self.changeParentCb.currentText
        print("CHANGE PARENT", imobj_name, "cb count", self.changeParentCb.count)
        imobj = mh.getImobjectByName(imobj_name) if imobj_name is not None else None

        self.selectedImobject.change_parent(imobj)


    def introAnimationHandler(self, i):
        if self.selectedImobject is None:
            return 

        # print('CHANGE INTRO', self.selectedImobject.__class__.__name__, i)

        imobject = self.selectedImobject
        if imobject.introAnim is not None:
            imobject.addedState.animations.remove(imobject.introAnim)
        else:
            imobject.addedState.added.remove(imobject)

        self.scene_model.remove(imobject)
        match i:
            case 0:
                imobject.introAnim = None
            case 1:
                imobject.introAnim = ICreate(imobject)
            case 2:
                imobject.introAnim = IFadeIn(imobject)

        if imobject.introAnim is not None:
            imobject.addedState.animations.append(imobject.introAnim)
            self.scene_model.playCopy(imobject.introAnim, imobject.addedState)
        else:
            imobject.addedState.added.add(imobject)
            self.scene_model.addCopy(imobject)
