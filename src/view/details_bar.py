import sys
from intermediate.ianimation import ICreate, IFadeIn
from intermediate.imobject import IGroup, INone
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
    QGroupBox,
    QFormLayout,
    QSpinBox,
    QDoubleSpinBox,
    QColorDialog,
    QMessageBox,
    QErrorMessage,
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

TOP_WIDGETS_NUM = 1 #stretch n groupbox
class DetailsBar(QWidget):
    def __init__(self, scene_model, fsm_model):
        super().__init__()

        self.scene_model = scene_model
        self.fsm_model = fsm_model

        self.selectedImobject = INone()

        self.setWindowTitle(" ")

        self.geometry = QRect(1450, 250, 150, 600)

        self.layout = QVBoxLayout()

        self.animationRunTime = QDoubleSpinBox()
        self.animationRunTime.minimum = 0
        self.animationRunTime.suffix = "s"
        self.animationRunTime.valueChanged.connect(self.changeAnimationRunTimeHandler)
        self.animationRunTime.setValue(fsm_model.curr.run_time)
        # self.stateLabel = QLabel(f"State {fsm_model.curr.idx}")

        self.loopCb = QComboBox()
        self.loopCb.addItem("None")
        self.loopCb.addItems([f"State {n}" for n in range(1, fsm_model.end.idx)])
        self.loopCb.currentIndexChanged.connect(self.loopStateChangeHandler)

        self.loopTimes = QSpinBox()
        self.loopTimes.minimum = 0
        self.loopTimes.suffix = " times"
        self.loopTimes.valueChanged.connect(self.changeLoopTimesHandler)

        self.stateGroupBox = QGroupBox(f"State {fsm_model.curr.idx}")
        stateLayout = QFormLayout()
        stateLayout.addRow(QLabel("Run time:"), self.animationRunTime)
        stateLayout.addRow(QLabel("Loop to:"), self.loopCb)
        stateLayout.addRow(QLabel("for:"), self.loopTimes)
        
        self.stateGroupBox.setLayout(stateLayout)
        self.layout.addWidget(self.stateGroupBox)
        self.layout.addStretch()
        self.emptyLabel = QLabel("nothing selected")
        self.layout.addWidget(self.emptyLabel)
        self.layout.addStretch()
        
        self.nameEdit = QLineEdit()
        self.nameEdit.setText(mh.getName(self.selectedImobject))
        self.nameEdit.editingFinished.connect(self.nameEditHandler)

        self.introCb = QComboBox()
        self.introCb.addItems(["None", "Create", "FadeIn"])
        self.introCb.currentIndexChanged.connect(self.introAnimationHandler)

        self.changeColorBtn = QPushButton("change colour")
        self.changeColorBtn.clicked.connect(self.changeColourBtnHandler)

        self.scaleBox = QDoubleSpinBox()
        self.scaleBox.minimum = 0
        self.scaleBox.valueChanged.connect(self.scaleBoxHandler)

        removeBtn = QPushButton("remove mobject")
        removeBtn.clicked.connect(self.removeMobjectHandler)

        self.groupCb = QComboBox()
        self.groupCb.currentIndexChanged.connect(self.groupCbHandler)

        self.newGroupBtn = QPushButton("+")
        self.newGroupBtn.clicked.connect(self.newGroupBtnHandler)

        self.groupRow = QHBoxLayout()
        self.groupRow.addWidget(self.groupCb)
        self.groupRow.addWidget(self.newGroupBtn)
        
        self.mobjGroupBox = QGroupBox(f"Selected: {mh.getName(self.selectedImobject)}")
        mobjLayout = QFormLayout()
        mobjLayout.addRow(QLabel("Name:"), self.nameEdit)
        mobjLayout.addRow(QLabel("Appear animation:"), self.introCb)
        mobjLayout.addRow(QLabel("Colour:"), self.changeColorBtn)
        mobjLayout.addRow(QLabel("Scale:"), self.scaleBox)
        mobjLayout.addRow(QLabel("Grouping:"), self.groupRow)
        mobjLayout.addRow(QLabel("Remove:"), removeBtn)
        self.mobjGroupBox.setLayout(mobjLayout)

        self.all_widgets = (self.mobjGroupBox, )

        # Tree widgets
        self.changeParentCb = QComboBox()
        self.changeParentCb.addItem("None")
        self.changeParentCb.currentIndexChanged.connect(self.changeParentHandler)

        self.changeNodeText = QLineEdit()
        self.changeNodeText.editingFinished.connect(self.changeNodeTextHandler)

        self.addChildBtn = QPushButton("add child")

        
        self.treeGroupBox = QGroupBox("Tree attributes")
        treeLayout = QFormLayout()
        treeLayout.addRow(QLabel("Node text:"), self.changeNodeText)
        treeLayout.addRow(QLabel("Parent:"), self.changeParentCb)
        treeLayout.addRow(QLabel("Add child:"), self.addChildBtn)
        self.treeGroupBox.setLayout(treeLayout)


        # self.tree_widgets = (self.changeNodeText, self.changeParentCb, self.addChildBtn, )
        self.tree_widgets = (self.treeGroupBox, )
    

        # Text widgets
        self.changeMarkupText = MarkupTextEdit(self)

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
        # fsm_model.selectedMobjectChange.connect()
        
        self.setLayout(self.layout)

    def refresh(self, imobject=None):
        # print('REFRESH', imobject)
        if imobject == self.selectedImobject and self.currIdx == self.fsm_model.curr.idx:
            return #nothing happened 
        if imobject is None:
            imobject = self.selectedImobject
        self.currIdx = self.fsm_model.curr.idx
        self.clearItems()
        self.selectedImobject = imobject
        self.addItems(imobject)



    def addItems(self, imobject):
        self.stateGroupBox.title = f"State {self.fsm_model.curr.idx}"
        self.animationRunTime.setValue(self.fsm_model.curr.run_time)
        self.loopCb.addItem("None")
        self.loopCb.addItems([f"State {n}" for n in range(1, self.fsm_model.end.idx)])
        self.loopCb.setCurrentIndex(self.loopCb.findText(f"State {self.fsm_model.curr.loop[0]}") if self.fsm_model.curr.loop is not None else 0)
        self.loopCb.blockSignals(False)
        if isinstance(imobject, INone):
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
                self.changeParentCb.blockSignals(False)
                self.changeNodeText.setText(mh.getCopy(imobject.label).text)
                self.changeNodeText.blockSignals(False)
            case IMarkupText() | IMathTex():
                for w in self.text_widgets:
                    self.layout.insertWidget(self.layout.count()-1, w)
                    
                self.changeMarkupText.setText(imobject.text)
                self.changeMarkupText.blockSignals(True)
                

                if isinstance(imobject, IMarkupText):
                    self.textEditLayout = QHBoxLayout()
                    for w in self.text_edits:
                        self.textEditLayout.addWidget(w)
                    self.layout.insertLayout(self.layout.count()-1, self.textEditLayout)

        
        self.mobjGroupBox.title = f"Selected: {mh.getName(imobject)}"
        # print("REFRESHED INTRO", imobject.introAnim.__class__.__name__ if imobject.introAnim is not None else 'None')
        self.introCb.blockSignals(True)
        self.introCb.setCurrentIndex(self.introCb.findText(imobject.introAnim.__class__.__name__[1:]) if imobject.introAnim is not None else 0)
        self.introCb.blockSignals(False)

        self.groupCb.addItem("None")
        self.groupCb.addItems([mh.getName(im) for im in mh.getGroups()])
        self.groupCb.setCurrentIndex(self.groupCb.findText(mh.getName(imobject.group) if imobject.group is not None else "None"))
        self.groupCb.blockSignals(False)

        self.scaleBox.blockSignals(True)
        self.scaleBox.value = self.fsm_model.get_curr_scale(imobject)
        self.scaleBox.blockSignals(False)

        self.nameEdit.setText(mh.getName(self.selectedImobject))
        self.nameEdit.blockSignals(False)

        # self.layout.addStretch()
    
    def clearItems(self):
        self.changeNodeText.blockSignals(True)
        self.nameEdit.blockSignals(True)
        self.changeMarkupText.blockSignals(True)
        self.loopCb.blockSignals(True)
        self.groupCb.blockSignals(True)
        for i in range(self.layout.count()-2, TOP_WIDGETS_NUM, -1): 
            child = self.layout.itemAt(i).widget()
            # print("clearing " + child.__class__.__name__ if child is not None else "NONE")
            if child is None:
                child = self.layout.itemAt(i).layout()
            if child is not None:
                child.setParent(None)

        #clear sublayout
        for i in reversed(range(self.textEditLayout.count())): 
            child = self.textEditLayout.itemAt(i).widget().setParent(None)


        if isinstance(self.selectedImobject, INode):
            self.addChildBtn.clicked.disconnect(self.selectedImobject.spawn_child)
            self.changeParentCb.blockSignals(True)
            self.changeParentCb.clear()

        self.loopCb.clear()
        self.groupCb.clear()

    def highlightMarkupText(self, highlight):
        if isinstance(self.selectedImobject, INone):
            return

        cursor = self.changeMarkupText.textCursor()
        self.selectedImobject.handleBold(cursor.selectionStart(), cursor.selectionEnd(), highlight)

    def loopStateChangeHandler(self, i):
        if self.changeParentCb.count == 0 or not self.loopCb.currentText:
            return 

        if self.loopCb.currentText == "None":
            self.fsm_model.curr.loop = None
        else:
            state_num = int(self.loopCb.currentText[6:])
            if not self.loopTimes.text:
                self.loopTimes.setValue(1)

            self.fsm_model.curr.loop = (state_num, 1)
            self.fsm_model.curr.loopCnt = 1

    def changeLoopTimesHandler(self, value):
        self.fsm_model.curr.loopCnt = value

    def changeMarkupTextHandler(self):
        if isinstance(self.selectedImobject, INone):
            return
        
        text = self.changeMarkupText.plainText
        self.selectedImobject.changeText(text)
        self.selectedImobject.editedAt = self.fsm_model.curr.idx 

    def changeNodeTextHandler(self):
        text = self.changeNodeText.text
        self.selectedImobject.change_label_text(text)
        self.selectedImobject.editedAt = self.fsm_model.curr.idx 

    def changeAnimationRunTimeHandler(self, value):
        self.fsm_model.curr.run_time = value

    def changeParentHandler(self, i):
        if self.changeParentCb.count == 0 or not isinstance(self.selectedImobject, INode):
            return 

        # print("CHANGE PARENT")
        imobj_name = self.changeParentCb.currentText
        imobj = mh.getImobjectByName(imobj_name) if imobj_name is not None else None

        self.selectedImobject.change_parent(imobj)


    def introAnimationHandler(self, i):
        if isinstance(self.selectedImobject, INone):
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
            # imobject.addedState.playCopy(imobject.introAnim, self.scene_model.scene)
        else:
            imobject.addedState.added.add(imobject)
            self.scene_model.addCopy(imobject)

    def removeMobjectHandler(self):
        self.fsm_model.instant_remove_obj_at_curr(self.selectedImobject)
        self.refresh()

    def newGroupBtnHandler(self):
        group = IGroup()
        self.fsm_model.instant_add_object_to_curr(group, select=False)
        mh.groups.add(group)

        self.refresh() # show new igroup in combobox

    def groupCbHandler(self, i):
        if isinstance(self.selectedImobject, INone):
            return

        imobject = self.selectedImobject
        mobject = mh.getCopy(imobject)
        if imobject.group is not None:
            mh.getCopy(imobject.group).remove(mobject)
            self.scene_model.scene.add(mobject)

        group_name = self.groupCb.currentText
        if group_name != "None":
            igroup = mh.getImobjectByName(group_name)
            group = mh.getCopy(igroup)

            igroup.add(imobject)
            self.fsm_model.curr.calledMobjectFunctions[igroup]['add'].add(imobject)

            self.scene_model.unselect_mobjects()
        else:
            pass # TODO: tabs for each child
            
    def changeColourBtnHandler(self):
        color = QColorDialog.getColor()

        if color.isValid():
            imobject = self.selectedImobject
            mcopy = mh.getCopy(imobject)

            mcopy.set_color(color.name())
            imobject.colorChanged = True
            self.scene_model.selected[mcopy] = color.name()
            target = mcopy.copy()
            
            self.fsm_model.edit_transform_target(imobject, target, color=color.name())

    def scaleBoxHandler(self, value):
        imobject = self.selectedImobject
        mcopy = mh.getCopy(imobject)

        old_scale = self.fsm_model.get_curr_scale(imobject)
        new_scale = self.fsm_model.clean_scale(value)
        mcopy.scale(new_scale / old_scale)
        target = mcopy.copy()
        
        self.fsm_model.edit_transform_target(imobject, target, scale=new_scale)

    def nameEditHandler(self):

        new_name = self.nameEdit.text
        if not mh.setName(self.selectedImobject, new_name):
            msg = QMessageBox()
            msg.setWindowTitle("Manimate")
            msg.text = "Name is already in use!"
            msg.icon = QMessageBox.Critical
            msg.standardButtons = QMessageBox.Ok
            msg.defaultButton = QMessageBox.Ok

            conflictImobj = mh.getImobjectByName(new_name)
            msg.detailedText = f"There is another {conflictImobj.__class__.__name__} with the same name {new_name}."

            msg.exec_()

        self.refresh()