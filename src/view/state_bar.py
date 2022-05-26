import sys
from models.fsm_model import FsmModel
import moderngl
from manim import *
from manim.opengl import *
from manim.renderer.opengl_renderer import OpenGLRenderer

from PySide6.QtGui import QOpenGLContext, QSurfaceFormat, QPen, QColor, QPainter
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot, QRect
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSlider,
    QLineEdit,
    QStyleOptionSlider
)
from __feature__ import true_property
from pathlib import Path
import moderngl_window as mglw
from moderngl_window.context.pyside2.window import Window as PySideWindow
from moderngl_window.timers.clock import Timer

class TimeSlider(QSlider):
    def paintEvent(self, ev):
        super(TimeSlider, self).paintEvent(ev)

        style = QApplication.style()
        opt = QStyleOptionSlider()
        handle = style.subControlRect(style.CC_Slider, opt, style.SC_SliderHandle)

        p = QPainter(self)

        # custom ticks to make discreteness obvious
        interval = self.tickInterval
        if (interval == 0):
            interval = self.pageStep

        tp = self.tickPosition
        if (tp != QSlider.TickPosition.NoTicks):
            for i in range(self.minimum, self.maximum + 1, interval):
                if self.minimum == self.maximum:
                    return

                x = round((i - self.minimum) / (self.maximum - self.minimum) * (self.width - handle.width()) + (handle.width() / 2.0)) - 1
                h = 2
                p.setPen(QColor("white"))
                if (tp == QSlider.TickPosition.TicksBothSides or tp == QSlider.TickPosition.TicksAbove):
                    y = self.rect.top()
                    p.drawLine(x, y, x, y + h)

                if (tp == QSlider.TickPosition.TicksBothSides or tp == QSlider.TickPosition.TicksBelow):
                    y = self.rect.bottom()
                    p.drawLine(x, y, x, y - h)
                
    
class StateWidget(QWidget):
    def __init__(self, scene_model, fsm_model):
        def timeChangeHandler(value):
            scene_model.unselect_mobjects()
            label.setText(f"{value}/{timeSlider.maximum}")
            fsm_model.set_state_number(value)

        def stateChangeHandler(value, length):
            timeSlider.maximum = length
            timeSlider.setValue(value)
            label.setText(f"{value}/{length}")




        super().__init__()

        self.setWindowTitle(" ")
        self.geometry = QRect(550, 800, 900, 100)

        # button1 = QPushButton("manim it")
        # button1.clicked.connect(lambda : self.manim_run())
        layout = QVBoxLayout()

        videoButtons = QHBoxLayout()
        sliderButtons = QHBoxLayout()

        runBtn = QPushButton("Play")
        runBtn.clicked.connect(lambda : fsm_model.run())

        stopBtn = QPushButton("Pause")
        stopBtn.clicked.connect(lambda : fsm_model.stop())

        videoButtons.addStretch()
        videoButtons.addWidget(runBtn)
        videoButtons.addWidget(stopBtn)
        videoButtons.addStretch()

        addframeBtn = QPushButton("+")
        addframeBtn.clicked.connect(lambda : fsm_model.add_state())
        delframeBtn = QPushButton("-")
        delframeBtn.clicked.connect(lambda : fsm_model.del_state())

        exportBtn = QPushButton("Export")
        exportBtn.clicked.connect(lambda : fsm_model.export())

        timeSlider = TimeSlider()
        timeSlider.setOrientation(Qt.Horizontal)
        timeSlider.tickInterval = 1
        timeSlider.maximum = 1
        timeSlider.minimum = 1
        timeSlider.tickPosition = QSlider.TickPosition.TicksBelow
        timeSlider.value = 1
        timeSlider.valueChanged.connect(timeChangeHandler)

        label = QLabel("1/1")

        fsm_model.stateChange.connect(stateChangeHandler)

        for w in (timeSlider, label, addframeBtn, delframeBtn, exportBtn):
            sliderButtons.addWidget(w)
        

        
        layout.addLayout(videoButtons)
        layout.addLayout(sliderButtons)
        self.setLayout(layout)