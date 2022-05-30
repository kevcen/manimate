from manim import *
from manim.utils.space_ops import shoelace

from IPython import get_ipython
import pickle
from PySide6.QtGui import QOpenGLContext, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QSizePolicy,
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
import threading

from intermediate.itree import IParentEdge 
import models.mobject_helper as mh
   


def point_to_mobject(self, point, search_set=None):
    # E.g. if clicking on the scene, this returns the top layer mobject
    # under a given point
    if search_set is None:
        search_set = self.mobjects

    print("SELECT OBJECTS NUMBER", len(search_set))
    for mobject in reversed(search_set):
        imobject = mh.getOriginal(mobject)
        if imobject is not None and mobject.is_point_touching(point) and imobject.allowed_to_select:
            return mobject
    return None

Scene.point_to_mobject = point_to_mobject

class Test(Scene):
    def construct(self):
        self.mouse_is_down = False
        self.clicked_point = None

        self.interactive_embed()


    def mouse_move_event(self, point, d_point):
        super().on_mouse_motion(point, d_point)
        # print(d_point)
        self.mouse_point.move_to(point)
        # self.delta_point.move_to(d_point)
        from PySide2.QtCore import Qt
        
        if self.mouse_is_down:
            self.handler.move_selected_by(point - self.clicked_point)
            self.clicked_point = point

    def on_mouse_press(self, point, mouse_button, modifiers):
        super().on_mouse_press(point, mouse_button, modifiers)
        if mouse_button == "LEFT":
            # self.mouse_drag_point.move_to(point)
            self.clicked_point = point
            self.mouse_is_down = True
            # self.mouse_point.move_to(point)
            mcopy = self.point_to_mobject(point)
            if mcopy is None:
                return
            ctrldown = modifiers & Qt.ControlModifier != 0
            self.handler.set_selected_mobject(mcopy, ctrldown)

        if mouse_button == "RIGHT":
            self.handler.unselect_mobjects()

    def on_mouse_release(self, point, mouse_button, modifiers):
        if mouse_button == "LEFT":
            #add animation to state
            self.handler.confirm_selected_move(point)

            self.mouse_is_down = False



    

            
