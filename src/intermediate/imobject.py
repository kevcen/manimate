from manim import *
import html
import models.mobject_helper as mh


class IMobject:
    def __init__(self, mobject, parentImobject=None):
        self.mobject = mobject #mobject to be only used as a initial target
        self.addedState = None 
        self.removedState = None
        self.introAnim = None
        self.isDeleted = False
        self.parentImobject = parentImobject
        self.editedAt = None
        self.group = None
        self.allowed_to_select = True
        self.scale = 1.0
        self.move_to = None
        self.colorChanged = False

    def declStr(self):
        return f"{self.mobject.__class__.__name__}()"


# Class representing no selected object
class INone(IMobject):
    def __init__(self):
        super().__init__(None)

class IGroup(IMobject):
    def __init__(self):
        super().__init__(VGroup())
        self.vgroup_children = set()
    
    def add(self, imobject):
        mobject, group = mh.getCopy(imobject), mh.getCopy(self)
        imobject.group = self

        self.vgroup_children.add(imobject)
        group.add(mobject)

    def childrenStr(self):
        childnames = []
        # for imobject in self.vgroup_children:
        #     childnames.append(mh.getName(imobject))
        
        return ', '.join(childnames)

    def declStr(self):
        return f"VGroup({self.childrenStr()})"

class ICircle(IMobject):
    def __init__(self, color=RED, radius=None, parentImobject=None):
        super().__init__(Circle(color=color, radius=radius), parentImobject=parentImobject)
        self.color = color
        self.radius = radius

    def declStr(self):
        return f"Circle(color=\"{self.color}\", radius={self.radius})"

class ISquare(IMobject):
    def __init__(self):
        super().__init__(Square())

class IStar(IMobject):
    def __init__(self):
        super().__init__(Star())

class ITriangle(IMobject):
    def __init__(self):
        super().__init__(Triangle())



