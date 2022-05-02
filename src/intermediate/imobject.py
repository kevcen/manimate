from manim import *

class IMobject:
    def __init__(self, mobject, parentImobject=None):
        self.mobject = mobject
        self.addedState = None 
        self.removedState = None
        self.introAnim = None
        self.movable = True
        self.isDeleted = False
        self.parentImobject = parentImobject

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

class IText(IMobject):
    def __init__(self, text, parentImobject=None):
        self.label = Text(text)
        super().__init__(self.label, parentImobject=parentImobject)

        self.label.set_color(RED)
        self.text = text

    def copyWith(self, mobject):
        pass
