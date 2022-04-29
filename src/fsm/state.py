
from manim import *
from bidict import bidict
from collections import defaultdict

from intermediate.ianimation import ITransform

class State:
    def __init__(self, animations=None):
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

    def addTransform(self, imobject):
        """
        PRE: called only after state has a target for the transform
        """
        assert imobject in self.targets

        print('add transform')

        if imobject not in self.transforms:
            self.transforms[imobject] = ITransform(imobject)
            self.animations.append(self.transforms[imobject])
        
        