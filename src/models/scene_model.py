from fsm.generator import AnimationGenerator
from manim.utils.color import *
from manim import *
from PySide6.QtCore import (Signal, QObject)

from intermediate.imobject import IMobject
import models.mobject_helper as mh

"""
Handles any rendering on the manim scene
"""
class SceneHandler(QObject):
    selectedMobjectChange = Signal(IMobject)
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        scene.handler = self
        self.generator = AnimationGenerator()
        self.selected = {}
        self.state_handler = None #to set

    # For debugging purposes
    def playOne(self, anim, state):
        anim.run_time = 0
        self.scene.play(anim)

    def playCopy(self, anim, state):
        forward_anim = self.generator.forward(anim, state)
        forward_anim.run_time = 0
        self.scene.play(forward_anim)

    def addMobjects(self, mobjects):
        for imobject in mobjects:
            mcopy = mh.getCopy(imobject)
            self.scene.add(mcopy)

    def removeMobjects(self, mobjects):
        for imobject in mobjects:
            mcopy = mh.getCopy(imobject)
            print(mcopy)
            self.scene.remove(mcopy)

    def forwardAttributes(self, state):
        for imobject in state.changedMobjectAttributes:
            for attr_name, value in state.changedMobjectAttributes[imobject].items():
                setattr(imobject, attr_name, value)

    def reverseAttributes(self, state):
        for imobject in state.changedMobjectAttributes:
            for attr_name in state.changedMobjectAttributes[imobject]:
                value = None
                if attr_name in state.prev.changedMobjectAttributes[imobject]:
                    value = state.prev.changedMobjectAttributes[imobject][attr_name] 
                else:
                    value = state.revAttributes[imobject][attr_name]
                print(imobject, attr_name, value)
                setattr(imobject, attr_name, value)

    def play(self, state):
        self.addMobjects(state.added)
        self.removeMobjects(state.removed)
        self.forwardAttributes(state)
        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]

        if forward_anim:
            self.scene.play(*forward_anim)
        else:
            self.scene.wait(1)

    def playFast(self, state):
        self.addMobjects(state.added)
        self.removeMobjects(state.removed)
        self.forwardAttributes(state)
        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]
        for animation in forward_anim:
            animation.run_time = 0

        if forward_anim:
            self.scene.play(*forward_anim)

    def playRev(self, state):
        reversed_anim = [self.generator.reverse(instr, state) for instr in state.animations]
        
        for animation in reversed_anim:
            print(animation, animation.mobject)
            animation.run_time = 0

        if reversed_anim:
            self.scene.play(*reversed_anim)

        
        self.addMobjects(state.removed)
        self.removeMobjects(state.added)
        self.reverseAttributes(state)

    ## debugging
    def replay(self, state):
        reversed_anim = [self.generator.reverse(instr, state) for instr in state.animations]

        for animation in reversed_anim:
            animation.run_time = 0

        if reversed_anim:
            self.scene.play(*reversed_anim)

        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]
        for animation in forward_anim:
            animation.run_time = 0

        if forward_anim:
            self.scene.play(*forward_anim)

    def add(self, imobject):
        self.scene.add(mh.getCopy(imobject))

    def remove(self, imobject):
        self.scene.remove(mh.getCopy(imobject))

    """ Selection functions """
    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()
        self.selected[mobject] = mobject.get_color()

        mobject.set_color(WHITE)
        self.state_handler.capture_prev(mobject)

        imobject = mh.getOriginal(mobject)
        print(imobject)
        self.selectedMobjectChange.emit(imobject)


    def unselect_mobjects(self, signal=True):
        for mobject, color in self.selected.items():
            mobject.set_color(color)

        self.selected = {}

        if signal: # emit signal for widgets
            self.selectedMobjectChange.emit(None)

    """" Movement functions """
    # TODO: refactor non-scene related functions out
    def confirm_selected_move(self, point):
        for mcopy in self.selected:
            self.state_handler.confirm_move(mcopy, point)

    def created_at_curr_state_with_anim(self, mcopy):
        imobject = mh.getOriginal(mcopy)

        if imobject is None:
            return True #block any interaction with it

        return self.state_handler.created_at_curr_state_with_anim(imobject)

    def move_selected_to(self, point):
        if not self.selected:
                return
        
        for mobject in self.selected:
            mobject.move_to(point)