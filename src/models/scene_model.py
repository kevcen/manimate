from manim.utils.color import *
from manim import *
from PySide6.QtCore import Signal, QObject

from intermediate.imobject import IMobject, INone
from intermediate.itext import IMarkupText
import models.mobject_helper as mh



class SceneModel(QObject):
    """
    Handles any rendering on the manim scene
    """

    selectedMobjectChange = Signal(IMobject)

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        scene.handler = self
        # generator = AnimationGenerator()
        self.selected = {}
        self.fsm_model = None  # to set

    def set_fsm_model(self, fsm_model):
        self.fsm_model = fsm_model

    def add_copy(self, imobject):
        self.scene.add(mh.get_copy(imobject))

    def remove(self, imobject):
        self.scene.remove(mh.get_copy(imobject))

    """ Selection functions """

    def set_selected_mobject(self, mobject, ctrldown=False):
        # if not ctrldown: #TODO
        self.unselect_mobjects()

        imobject = mh.get_original(mobject)
        self.set_selected_imobject(imobject)

    def set_selected_imobject(self, imobject):
        if imobject.parent_imobject is not None:
            imobject = imobject.parent_imobject

        if imobject.group is not None:
            imobject = imobject.group

        mobject = mh.get_copy(imobject)

        self.selected[mobject] = mobject.get_color()

        if not isinstance(imobject, IMarkupText):
            mobject.set_color("#8fbc8f")

        self.fsm_model.curr.capture_prev(mobject)

        # print(imobject)
        self.selectedMobjectChange.emit(imobject)

    def unselect_mobjects(self):
        print("UNSELETED")
        for mobject, color in self.selected.items():
            if not isinstance(mobject, MarkupText):
                mobject.set_color(color)

        self.selected = {}

        self.selectedMobjectChange.emit(INone())

    """" Movement functions """
    # TODO: refactor non-scene related functions out
    def confirm_selected_move(self, point):
        for mcopy in self.selected:
            self.fsm_model.confirm_move(mcopy, point)

    def created_at_curr_state_with_anim(self, mcopy):
        imobject = mh.get_original(mcopy)

        if imobject is None:
            return True  # block any interaction with it

        return self.fsm_model.created_at_curr_state_with_anim(imobject)

    def move_selected_by(self, delta):
        if not self.selected:
            return
        # target = new_point.get_bounding_box_point(ORIGIN)
        # old = old_point.get_bounding_box_point(ORIGIN)
        for mobject in self.selected:
            # mobject.shift((target - old) * np.array([1, 1, 1]))
            mobject.shift(delta)
