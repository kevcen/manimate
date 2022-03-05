import sys
from model.state_handler import StateHandler
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
            label.setText(f"{value}/{timeSlider.maximum}")
            state_handler.set_state_number(value)

        def stateChangeHandler(value, length):
            timeSlider.maximum = length
            timeSlider.setValue(value)
            label.setText(f"{value}/{length}")




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


        frameBtn = QPushButton("new frame")
        frameBtn.clicked.connect(lambda : state_handler.add_state())

        exportBtn = QPushButton("export")
        exportBtn.clicked.connect(lambda : state_handler.export())

        timeSlider = QSlider()
        timeSlider.setOrientation(Qt.Horizontal)
        timeSlider.tickInterval = 1
        timeSlider.maximum = 1
        timeSlider.minimum = 1
        timeSlider.tickPosition = QSlider.TickPosition.TicksBelow
        timeSlider.value = 1
        timeSlider.valueChanged.connect(timeChangeHandler)

        label = QLabel("1/1")

        state_handler.stateChange.connect(stateChangeHandler)

        for w in (timeSlider, label, runBtn, stopBtn, frameBtn, exportBtn):
            layout.addWidget(w)
        
        self.setLayout(layout)