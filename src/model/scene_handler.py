from fsm.generator import AnimationGenerator
from manim.utils.color import *
from manim import *
from PySide6.QtCore import (Signal, QObject)

class SceneHandler(QObject):
    selectedMobjectChange = Signal(Mobject)

    def __init__(self, scene, mobject_handler):
        super().__init__()
        self.scene = scene
        scene.handler = self
        self.generator = AnimationGenerator(mobject_handler)
        self.selected = None
        self.state_handler = None #to set
        self.mobject_handler = mobject_handler

    def playOne(self, anim, state):
        # forward_anim = self.generator.forward(anim, state)
        # forward_anim.run_time = 0
        # self.scene.play(forward_anim)
        # anim = anim.copy()
        anim.run_time = 0
        self.scene.play(anim)

    def playCopy(self, anim, state):
        forward_anim = self.generator.forward(anim, state)
        forward_anim.run_time = 0
        self.scene.play(forward_anim)

    def play(self, state):
        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]

        if forward_anim:
            self.scene.play(*forward_anim)
        else:
            self.scene.wait(1)


    def playFast(self, state):
        forward_anim = [self.generator.forward(anim, state) for anim in state.animations]
        for animation in forward_anim:
            animation.run_time = 0.1

        if forward_anim:
            self.scene.play(*forward_anim)

    def playRev(self, state):
        reversed_anim = [self.generator.reverse(instr, state) for instr in state.animations]
        
        for animation in reversed_anim:
            animation.run_time = 0.1

        if reversed_anim:
            self.scene.play(*reversed_anim)

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

    def reset(self):
        self.scene.clear()
        self.scene.render()

    def add(self, mobject):
        self.scene.add(mobject)

    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()

        # self.selected[mobject] = mobject.get_color()
        self.selected = mobject
        mobject.set_color(WHITE)

        self.selectedMobjectChange.emit(mobject)

        self.state_handler.select_mobject(mobject)

        #create copy of target to prepare for any movements
        # self.state_handler.create_target(mboject)


    def unselect_mobjects(self, signal=False):
        # for mobj, color in list(self.selected.items()):
        #     mobj.set_color(color)
        #     del self.selected[mobj]
        self.selected = None

        if signal:
            self.selectedMobjectChange.emit(None)
        # pass

    def move_selected_object(self):
        # if not self.selected:
        #     return #nothing selected 
        
        # mcopy = list(self.selected.keys())[0] #assume only 1 object is selected for now
        # if mcopy not in self.mobject_handler.originals:
        #     return 

        mcopy = self.selected
        mcopy.set_color(YELLOW_C)

        self.state_handler.move_to_target(mcopy)
            