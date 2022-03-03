
from manim import *
from bidict import bidict

class State:
    def __init__(self, animations=None):
        self.next = None #next state
        self.prev = None #previous state
        self.animations = animations if animations else [] #list of animations to play
        self.targets = bidict()
        self.transforms = {}

    def getTransform(self, mobject):
        """
        PRE: called only after next state has a target for the transform
        """
        assert mobject in self.next.targets

        if mobject not in self.transforms:
            self.transforms[mobject] = Transform(mobject, self.next.targets[mobject])
            self.animations.append(self.transforms[mobject])
        
        return self.transforms[mobject]
        