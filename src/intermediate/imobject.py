from manim import *

class IMobject:
    def __init__(self, mobject):
        self.mobject = mobject
        self.addedState = None 
        self.removedState = None
        self.introAnim = None
        self.movable = True

    def copyWith(self, mobject):
        return IMobject(mobject)

class ICircle(IMobject):
    def __init__(self):
        super().__init__(Circle())

    def copyWith(self, mobject):
        return ICircle(mobject)


class ISquare(IMobject):
    def __init__(self):
        super().__init__(Square())

    def copyWith(self, mobject):
        return ISquare(mobject)

