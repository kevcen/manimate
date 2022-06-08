from manim import *
import models.mobject_helper as mh
import copy
from collections import defaultdict

class IMobject:
    """
    Intermediate mobject class
    """
    def __init__(self, mobject, parent_imobject=None, key_imobject=None):
        self.mobject = mobject  # mobject to be only used as a initial target
        self.added_state = None
        self.removed_state = None
        self.intro_anim = None
        self.is_deleted = False
        self.parent_imobject = parent_imobject
        self.edited_at = None
        self.group = None
        self.allowed_to_select = True
        self.past_scale = 1.0
        self.past_point = None
        self.color_changed = False
        self.key_imobject = key_imobject if key_imobject is not None else self
        # self.rev_attributes = defaultdict(lambda: {})
        self.changed_attributes = defaultdict(lambda: {})

    def decl_str(self):
        return f"{self.mobject.__class__.__name__}()"

    def copy(self):
        cimobj = copy.copy(self)
        cimobj.key_imobject = self.key_imobject
        return cimobj


class INone(IMobject):
    """
    Intermediate mobject class representing no selected object
    """
    def __init__(self):
        super().__init__(None)


class IGroup(IMobject):
    """
    Intermediate mobject class representing a grouping
    """
    def __init__(self, fsm_model, key_imobject=None):
        super().__init__(VGroup(), key_imobject=key_imobject)
        self.fsm_model = fsm_model
        self.vgroup_children = set()

    def add(self, imobject):
        print("ADD TO IGROUP")
        mobject, group = mh.get_copy(imobject), mh.get_copy(self)
        imobject.group = self

        self.vgroup_children.add(imobject)
        group.add(mobject)
        # if self in state.prev.targets:
        #     state.prev.get_target(self)
        #     self.fsm_model

    def children_str(self):
        childnames = []
        # for imobject in self.vgroup_children:
        #     childnames.append(mh.getName(imobject))

        return ", ".join(childnames)

    def decl_str(self):
        return f"VGroup({self.children_str()})"


class ICircle(IMobject):
    """
    Intermediate Circle class
    """
    def __init__(self, color=RED, radius=None, parent_imobject=None, key_imobject=None):
        super().__init__(
            Circle(color=color, radius=radius), parent_imobject=parent_imobject, key_imobject=key_imobject
        )
        self.color = color
        self.radius = radius

    def decl_str(self):
        return f'Circle(color="{self.color}", radius={self.radius})'


class ISquare(IMobject):
    """
    Intermediate Square class
    """
    def __init__(self, key_imobject=None):
        super().__init__(Square(), key_imobject=key_imobject)


class IStar(IMobject):
    """
    Intermediate Star class
    """
    def __init__(self, key_imobject=None):
        super().__init__(Star(), key_imobject=key_imobject)


class ITriangle(IMobject):
    """
    Intermediate Triangle class
    """
    def __init__(self, key_imobject=None):
        super().__init__(Triangle(), key_imobject=key_imobject)
