from fsm.generator import AnimationGenerator
from manim.utils.color import *
from manim import *
from PySide6.QtCore import (Signal, QObject)

from intermediate.imobject import IMobject

"""
Handles any rendering on the manim scene
"""
class SceneHandler(QObject):
    selectedMobjectChange = Signal(IMobject)

    def __init__(self, scene, mobject_handler):
        super().__init__()
        self.scene = scene
        scene.handler = self
        self.generator = AnimationGenerator(mobject_handler)
        self.selected = {}
        self.state_handler = None #to set
        self.mobject_handler = mobject_handler

    # For debugging purposes
    def playOne(self, anim, state):
        anim.run_time = 0
        self.scene.play(anim)

    def playCopy(self, anim, state):
        forward_anim = self.generator.forward(anim, state)
        forward_anim.run_time = 0
        self.scene.play(forward_anim)

    def play(self, state):
        self.addMobjects(state)
        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]

        if forward_anim:
            self.scene.play(*forward_anim)
        else:
            self.scene.wait(1)

    def addMobjects(self, state):
        for imobject in state.added:
            mcopy = self.mobject_handler.getCopy(imobject)
            self.scene.add(mcopy)

    def removeMobjects(self, state):
        for imobject in state.added:
            mcopy = self.mobject_handler.getCopy(imobject)
            self.scene.remove(mcopy)

    def playFast(self, state):
        self.addMobjects(state)
        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]
        for animation in forward_anim:
            animation.run_time = 0

        if forward_anim:
            self.scene.play(*forward_anim)

    def playRev(self, state):
        self.removeMobjects(state)
        reversed_anim = [self.generator.reverse(instr, state) for instr in state.animations]
        
        for animation in reversed_anim:
            animation.run_time = 0

        if reversed_anim:
            self.scene.play(*reversed_anim)

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
        self.scene.add(self.mobject_handler.getCopy(imobject))

    def remove(self, imobject):
        self.scene.remove(self.mobject_handler.getCopy(imobject))

    """ Selection functions """
    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()
        self.selected[mobject] = mobject.get_color()

        mobject.set_color(WHITE)
        self.state_handler.capture_prev(mobject)

        imobject = self.mobject_handler.getOriginal(mobject)
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

    def created_at_curr_state(self, mcopy):
        imobject = self.mobject_handler.getOriginal(mcopy)

        if imobject is None:
            return True #block any interaction with it

        return self.state_handler.created_at_curr_state(imobject)

    def move_selected_to(self, point):
        if not self.selected:
                return
        
        for mobject in self.selected:
            mobject.move_to(point)