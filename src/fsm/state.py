
from manim import *

class State:
    def __init__(self, animations=None):
        self.next = None #next state
        self.prev = None #previous state
        self.animations = animations if animations else [] #list of animation instructions
        # self.states = {} #mapping from mobject to state
        self.mobjects = []
        

        