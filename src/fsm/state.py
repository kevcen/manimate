
from manim import *
from bidict import bidict
from collections import defaultdict

from intermediate.ianimation import ITransform
import models.mobject_helper as mh

class State:
    def __init__(self, idx, animations=None):
        self.next = None #next state
        self.prev = None #previous state
        self.animations = animations if animations else [] #list of animations to play
        self.targets = bidict() # what the mobjects look like at this state at the end
        self.rev_targets = bidict()
        self.transforms = {}
        ## TODO: replace transforms by using prepare_anim on changedtargetattributes
        self.changedTargetAttributes = defaultdict(lambda: {})
        self.revAttributes = defaultdict(lambda: {})
        self.changedMobjectAttributes = defaultdict(lambda: {})
        self.added = set()
        self.removed = set()
        self.idx = idx

    def addTransform(self, imobject):
        """
        PRE: called only after state has a target for the transform
        """
        assert imobject in self.targets


        if imobject not in self.transforms:
            self.transforms[imobject] = ITransform(imobject)
            self.animations.append(self.transforms[imobject])

    def getTransform(self, imobject):
        return self.transforms[imobject] if imobject in self.transforms else None
        
    
    def capture_prev(self, mcopy, bypass=False):
        print('try capture', hex(id(self)))
        # capture previous frame for reverse if editable
        imobject = mh.getOriginal(mcopy)
        if bypass or imobject not in self.rev_targets: #if not already captured
            print('captured prev')
            target = self.find_prev_target(self.prev, imobject)
            if target is None:
                print('head state')
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