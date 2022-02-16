
from manim import *

class State:
    def __init__(self, animations):
        self.next = None #next state
        self.prev = None #previous state
        self.animations = animations #list of animation instructions
        # self.states = {} #mapping from mobject to state
        

        