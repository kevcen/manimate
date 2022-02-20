import sys
from fsm.state_handler import StateHandler
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot, QRect, QEventLoop
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QSlider,
    QLineEdit
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer


class StateWidget(QWidget):
    def __init__(self, scene_handler, state_handler):
        def timeChangeHandler(value):
            # self.timeSlider.setValue(value)
            label.setText(str(value))
            state_handler.set_state_number(value)

        def stateChangeHandler(value):
            self.timeSlider.setValue(value)
            label.setText(str(value))


        # def sliderReleaseHandler():
        #     # self.timeSlider.setValue(round(self.timeSlider.value))
        #     label.setText(str(self.timeSlider.value))

        super().__init__()

        self.setWindowTitle(" ")
        self.geometry = QRect(900, 800, 900, 100)

        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QHBoxLayout()


        runBtn = QPushButton("run")
        runBtn.clicked.connect(lambda : state_handler.run())

        stopBtn = QPushButton("stop")
        stopBtn.clicked.connect(lambda : state_handler.stop())

        self.timeSlider = QSlider()
        # QSlider.setTickInterval(self.timeSlider, 2)
        self.timeSlider.setOrientation(Qt.Horizontal)
        self.timeSlider.tickInterval = 1
        self.timeSlider.maximum = 2
        self.timeSlider.minimum = 0
        self.timeSlider.tickPosition = QSlider.TickPosition.TicksBelow
        self.timeSlider.valueChanged.connect(timeChangeHandler)
        # self.timeSlider.sliderReleased.connect(sliderReleaseHandler)

        label = QLabel("0")
        # label.setText(str(self.timeSlider.tickInterval))

        state_handler.stateChange.connect(stateChangeHandler)
        
        # self.manim.setFormat(format); # must be called before the widget or its parent window gets shown

        for w in (self.timeSlider, runBtn, stopBtn, label):
            layout.addWidget(w)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #232326; color: white")