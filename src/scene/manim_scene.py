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
        if mobject.is_point_touching(point) and imobject.allowed_to_select:
            return mobject
    return None

Scene.point_to_mobject = point_to_mobject

class Test(Scene):
    def construct(self):
        self.mouse_is_down = False
        # A = Dot([1, 0, 0])
        # B = Dot([0, 1, 0])
        # plane = always_redraw(
        #     lambda: NumberPlane().apply_matrix(np.array([A.get_center()[:2], B.get_center()[:2]]).T)
        # )
        # vecs = VGroup(
        #     always_redraw(lambda: Vector(A.get_center(), color=RED)),
        #     always_redraw(lambda: Vector(B.get_center(), color=GREEN)),
        # )
        # det = always_redraw(
        #     lambda: Polygon(ORIGIN, A.get_center(), A.get_center() + B.get_center(), B.get_center(), fill_opacity=0.4, color=YELLOW)
        # )
        # num = always_redraw(lambda: DecimalNumber(-shoelace(det.points)).to_corner(UL))
        # self.add(plane, det, vecs, num, A, B)

        self.interactive_embed()


    def mouse_move_event(self, point, d_point):
        super().on_mouse_motion(point, d_point)
        self.mouse_point.move_to(point)
        from PySide2.QtCore import Qt
        
        if self.mouse_is_down:
            self.handler.move_selected_to(self.mouse_point)

    def on_mouse_press(self, point, mouse_button, modifiers):
        super().on_mouse_press(point, mouse_button, modifiers)
        if mouse_button == "LEFT":
            self.mouse_is_down = True
            self.mouse_point.move_to(point)
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



    

            
