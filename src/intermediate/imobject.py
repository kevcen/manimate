from manim import *
import html
import models.mobject_helper as mh

class IMobject:
    def __init__(self, mobject, parentImobject=None):
        self.mobject = mobject
        self.addedState = None 
        self.removedState = None
        self.introAnim = None
        self.movable = True
        self.isDeleted = False
        self.parentImobject = parentImobject
        self.editedAt = None

    def copyWith(self, mobject):
        return IMobject(mobject)

class ICircle(IMobject):
    def __init__(self, color=RED, radius=None, parentImobject=None):
        super().__init__(Circle(color=color, radius=radius), parentImobject=parentImobject)
        

    def copyWith(self, mobject):
        return ICircle(mobject)


class ISquare(IMobject):
    def __init__(self):
        super().__init__(Square())

    def copyWith(self, mobject):
        return ISquare(mobject)


class IStar(IMobject):
    def __init__(self):
        super().__init__(Star())

class ITriangle(IMobject):
    def __init__(self):
        super().__init__(Triangle())

class IRegularPolygon(IMobject):
    def __init__(self, n=5):
        super().__init__(RegularPolygon(n))




