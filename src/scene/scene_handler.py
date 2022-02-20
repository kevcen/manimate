

from fsm.reverser import Reverser
from manim.utils.color import *

class SceneHandler:
    def __init__(self, scene=None):
        self.scene = scene
        self.reverser = Reverser()
        self.selected = {}

    def setScene(self, scene):
        self.scene = scene
        scene.handler = self

    def play(self, state):
        forward_anim = [self.reverser.forward(anim) for anim in state.animations]

        if forward_anim:
            self.scene.play(*forward_anim)
            # self.scene.wait()


    def playFast(self, state):
        forward_anim = [self.reverser.forward(anim) for anim in state.animations]
        for animation in forward_anim:
            animation.run_time = 0.1

        if forward_anim:
            self.scene.play(*forward_anim)

    def playRev(self, state):
        reversed_anim = [self.reverser.reverse(instr) for instr in state.animations]
        
        for animation in reversed_anim:
            animation.run_time = 0.1

        if reversed_anim:
            self.scene.play(*reversed_anim)

    def reset(self):
        self.scene.clear()
        self.scene.render()

    def add(self, mobject):
        self.scene.add(mobject)

    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()

        self.selected[mobject] = mobject.get_color()
        mobject.set_color(YELLOW_C)

    def unselect_mobjects(self):
        for mobj, color in self.selected.items():
            mobj.set_color(color)
            