
from email.policy import default
from manim import *
from bidict import bidict
from collections import defaultdict

from intermediate.ianimation import IApplyFunction, ITransform
import fsm.generator as generator
import models.mobject_helper as mh

# from manim.animation.animation import DEFAULT_ANIMATION_RUN_TIME

class State:
    def __init__(self, idx, animations=None):
        self.next = None #next state
        self.prev = None #previous state
        self.animations = animations if animations else [] #list of animations to play
        self.targets = bidict() # what the mobjects look like at this state at the end
        self.rev_targets = bidict()
        self.transforms = {}
        self.applyfunctions = {}
        ## TODO: replace transforms by using prepare_anim on calledTargetFunctions
        # imobject -> function -> set(args)
        self.calledMobjectFunctions = defaultdict(lambda: defaultdict(lambda: set()))
        self.calledTargetFunctions = defaultdict(lambda: defaultdict(lambda: set()))
        self.targetDeclStr = {}
        self.revAttributes = defaultdict(lambda: {})
        self.changedMobjectAttributes = defaultdict(lambda: {})
        self.added = set()
        self.removed = set()
        self.idx = idx
        self.run_time = 1.0
        self.loop = None # in form of (state, times)
        self.loopCnt = None


    def addTransform(self, imobject):
        """
        PRE: called only after state has a target for the transform
        """
        assert imobject in self.targets


        if imobject not in self.transforms:
            self.transforms[imobject] = ITransform(imobject)
            self.animations.append(self.transforms[imobject])

        return self.transforms[imobject]

    def getTransform(self, imobject):
        return self.transforms[imobject] if imobject in self.transforms else None
        
    def addApplyFunction(self, imobject):
        if imobject not in self.applyfunctions:
            self.applyfunctions[imobject] = IApplyFunction(imobject)
            self.animations.append(self.applyfunctions[imobject])

        return self.applyfunctions[imobject]

    def getApplyFunction(self, imobject):
        return self.applyfunctions[imobject] if imobject in self.applyfunctions else None

    # Capturing states for reverse
    def capture_prev(self, mcopy, bypass=False):
        # print('try capture', hex(id(self)))
        # capture previous frame for reverse if editable
        imobject = mh.getOriginal(mcopy)
        if bypass or imobject not in self.rev_targets: #if not already captured
            target = self.find_prev_target(self.prev, imobject)
            if target is None:
                return #we are in head state
                
            self.rev_targets[imobject] = target
            if imobject.editedAt is not None and imobject.editedAt < self.idx:
                imobject.editedAt = None #mark as handled 

    def find_prev_target(self, state, imobject):
        if state is None:
            return None 

        if imobject in state.targets:
            return state.targets[imobject].copy()
        return self.find_prev_target(state.prev, imobject)

    # Scene related functions
    def playOne(self, anim, scene):
        anim.run_time = 0
        scene.play(anim)

    def playCopy(self, anim, scene):
        forward_anim = generator.forward(anim, self)
        forward_anim.run_time = 0
        scene.play(forward_anim)

    def addMobjects(self, mobjects, scene):
        for imobject in mobjects:
            mcopy = mh.getCopy(imobject)
            scene.add(mcopy)

    def removeMobjects(self, mobjects, scene):
        for imobject in mobjects:
            mcopy = mh.getCopy(imobject)
            scene.remove(mcopy)

    def forwardAttributes(self):
        for imobject in self.changedMobjectAttributes:
            for attr_name, value in self.changedMobjectAttributes[imobject].items():
                setattr(imobject, attr_name, value)

    def reverseAttributes(self):
        for imobject in self.changedMobjectAttributes:
            for attr_name in self.changedMobjectAttributes[imobject]:
                value = None
                if attr_name in self.prev.changedMobjectAttributes[imobject]:
                    value = self.prev.changedMobjectAttributes[imobject][attr_name] 
                else:
                    value = self.revAttributes[imobject][attr_name]
                # print(imobject, attr_name, value)
                setattr(imobject, attr_name, value)

    def play(self, scene, fast=False):
        self.addMobjects(self.added, scene)
        self.removeMobjects(self.removed, scene)
        self.forwardAttributes()
        forward_anim = list(filter(None, map(lambda a: generator.forward(a, self), self.animations)))

        for animation in forward_anim:
            animation.run_time = self.run_time if not fast else 0

        if len(forward_anim) > 0:
            scene.play(*forward_anim)
        elif not fast:
            scene.wait(1)

    def playRev(self, scene):
        # print(f"rem {len(state.added)}, anim {len(state.animations)}")
        reversed_anim = list(filter(None, map(lambda a: generator.reverse(a, self), self.animations)))
        
        for animation in reversed_anim:
            # print('rev', animation, animation.mobject)
            animation.run_time = 0

        if len(reversed_anim) > 0:
            scene.play(*reversed_anim)

        
        self.addMobjects(self.removed, scene)
        self.removeMobjects(self.added, scene)
        self.reverseAttributes()

    ## debugging
    def replay(self, scene):
        reversed_anim = [generator.reverse(instr, self) for instr in self.animations]

        for animation in reversed_anim:
            animation.run_time = 0

        if reversed_anim:
            scene.play(*reversed_anim)

        forward_anim = [generator.forward(anim, self) for anim in self.animations]
        for animation in forward_anim:
            animation.run_time = 0

        if forward_anim:
            scene.play(*forward_anim)