from fsm.generator import AnimationGenerator
from manim.utils.color import *
from manim import *
from PySide6.QtCore import (Signal, QObject)

from intermediate.imobject import IMobject
from intermediate.itext import IMarkupText
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

    def setStateHandler(self, state_handler):
        self.state_handler = state_handler

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
        forward_anim = list(filter(None, map(lambda a: self.generator.forward(a, state), state.animations)))

        if len(forward_anim) > 0:
            self.scene.play(*forward_anim)
        else:
            self.scene.wait(1)

    def playFast(self, state):
        print(f"add {len(state.added)}, anim {len(state.animations)}")
        self.addMobjects(state.added)
        self.removeMobjects(state.removed)
        self.forwardAttributes(state)
        forward_anim = list(filter(None, map(lambda a: self.generator.forward(a, state), state.animations)))

        for animation in forward_anim:
            print('for', animation, animation.mobject)
            animation.run_time = 0

        if len(forward_anim) > 0:
            self.scene.play(*forward_anim)

    def playRev(self, state):
        print(f"rem {len(state.added)}, anim {len(state.animations)}")
        reversed_anim = list(filter(None, map(lambda a: self.generator.reverse(a, state), state.animations)))
        
        for animation in reversed_anim:
            print('rev', animation, animation.mobject)
            animation.run_time = 0

        if len(reversed_anim) > 0:
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

    def addCopy(self, imobject):
        self.scene.add(mh.getCopy(imobject))

    def remove(self, imobject):
        self.scene.remove(mh.getCopy(imobject))

    """ Selection functions """
    def set_selected_mobject(self, mobject):
        self.unselect_mobjects()
        imobject = mh.getOriginal(mobject)
        # print(mobject, imobject)
        print('select', hex(id(mobject)))
        if imobject.parentImobject is not None:
            imobject = imobject.parentImobject 
            mobject = mh.getCopy(imobject)
        
        self.selected[mobject] = mobject.get_color()

        if not isinstance(imobject, IMarkupText):
            mobject.set_color(WHITE)
            
        self.state_handler.curr.capture_prev(mobject)

        print(imobject)
        self.selectedMobjectChange.emit(imobject)


    def unselect_mobjects(self, signal=True):
        for mobject, color in self.selected.items():
            if not isinstance(mobject, MarkupText):
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