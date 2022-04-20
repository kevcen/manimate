from fsm.generator import AnimationGenerator
from manim.utils.color import *
from manim import *
from PySide6.QtCore import (Signal, QObject)

"""
Handles any rendering on the manim scene
"""
class SceneHandler(QObject):
    selectedMobjectChange = Signal(Mobject)

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
        for mobjects in state.added:
            self.scene.add(mobjects)

    def removeMobjects(self, state):
        for mobjects in state.added:
            self.scene.remove(mobjects)

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

    def add(self, mobject):
        self.scene.add(mobject)

    """ Selection functions """
    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()
        self.selected[mobject] = mobject.get_color()

        mobject.set_color(WHITE)
        self.state_handler.select_mobject(mobject)

        self.selectedMobjectChange.emit(mobject)


    def unselect_mobjects(self, signal=False):
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
        mobject = self.mobject_handler.getOriginal(mcopy)

        if mobject is None:
            return True #block any interaction with it

        return self.state_handler.created_at_curr_state(mobject)

    def move_selected_to(self, point):
        if not self.selected:
                return
        
        for mobject in self.selected:
            mobject.move_to(point)