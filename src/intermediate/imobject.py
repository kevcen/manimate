from manim import *

class IMobject:
    def __init__(self, mobject):
        self.mobject = mobject
        self.addedState = None 
        self.removedState = None
        self.introAnim = None

class ICircle(IMobject):
    def __init__(self):
        self.mobject = Circle()


class ISquare(IMobject):
    def __init__(self):
        self.mobject = Square()

