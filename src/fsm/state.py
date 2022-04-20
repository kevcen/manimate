
from manim import *
from bidict import bidict
from collections import defaultdict

from intermediate.ianimation import ITransform

class State:
    def __init__(self, animations=None):
        self.next = None #next state
        self.prev = None #previous state
        self.animations = animations if animations else [] #list of animations to play
        self.targets = bidict() # what the mobjects look like at this state initially
        self.transforms = {}
        self.changedTargetAttributes = defaultdict(lambda: {})
        self.added = set()

    def getTransform(self, imobject):
        """
        PRE: called only after next state has a target for the transform
        """
        assert imobject in self.next.targets

        if imobject not in self.transforms:
            self.transforms[imobject] = ITransform(imobject)
            self.animations.append(self.transforms[imobject])
        
        return self.transforms[imobject]
        