import fsm.generator as generator
from manim.utils.color import *
from manim import *
from PySide6.QtCore import (Signal, QObject)

from intermediate.imobject import IMobject, INone
from intermediate.itext import IMarkupText
import models.mobject_helper as mh

"""
Handles any rendering on the manim scene
"""
class SceneModel(QObject):
    selectedMobjectChange = Signal(IMobject)
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        scene.handler = self
        # generator = AnimationGenerator()
        self.selected = {}
        self.fsm_model = None #to set

    def setFsmModel(self, fsm_model):
        self.fsm_model = fsm_model

    # For debugging purposes

    def addCopy(self, imobject):
        self.scene.add(mh.getCopy(imobject))

    def remove(self, imobject):
        self.scene.remove(mh.getCopy(imobject))

    """ Selection functions """
    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()
        imobject = mh.getOriginal(mobject)
        # print(mobject, imobject)
        # print('select', hex(id(mobject)))
        self.set_selected_imobject(imobject)
        
    def set_selected_imobject(self, imobject):
        print("SELECT NEW OBJ")
        if imobject.parentImobject is not None:
            imobject = imobject.parentImobject
        
        mobject = mh.getCopy(imobject)
        
        self.selected[mobject] = mobject.get_color()

        if not isinstance(imobject, IMarkupText):
            mobject.set_color(BLUE_A)
            
        self.fsm_model.curr.capture_prev(mobject)

        # print(imobject)
        self.selectedMobjectChange.emit(imobject)

    def unselect_mobjects(self):
        print("UNSELECT")
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
        imobject = mh.getOriginal(mcopy)

        if imobject is None:
            return True #block any interaction with it

        return self.fsm_model.created_at_curr_state_with_anim(imobject)

    def move_selected_to(self, point):
        if not self.selected:
                return
        
        for mobject in self.selected:
            mobject.move_to(point)