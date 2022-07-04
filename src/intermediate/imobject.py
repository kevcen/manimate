from manim import *
import controllers.mobject_helper as mh


class IMobject:
    """
    Intermediate mobject class
    """

    def __init__(self, mobject, parent_imobject=None, user_defined=False):
        self.mobject = mobject  # mobject to be only used as a initial target
        self.added_state = None
        self.removed_state = None
        self.intro_anim = None
        self.is_deleted = False
        self.parent_imobject = parent_imobject
        self.edited_at = None
        self.group = None
        self.is_allowed_to_select = True
        self.past_scale = 1.0
        self.scale = 1.0
        self.past_point = None
        self.color_changed = None
        self.child_add_state = None
        self.user_defined = user_defined
        
    def allowed_to_select(self):
        return self.is_allowed_to_select

    def decl_str(self):
        return f"{self.mobject.__class__.__name__}()"



class INone(IMobject):
    """
    Intermediate mobject class representing no selected object
    """

    def __init__(self):
        super().__init__(None)


class IDependent(IMobject):
    """
    Intermediate abstract class representing mobjects that depend on others

    This is used purely for ordering of the writer.

    E.g. IParentEdge needs to be defined after INode
    """

    pass


class IGroup(IMobject):
    """
    Intermediate mobject class representing a grouping
    """

    def __init__(self):
        super().__init__(VGroup())
        self.vgroup_children = set()

    def add(self, imobject):
        mobject, group = mh.get_copy(imobject), mh.get_copy(self)
        imobject.group = self

        self.vgroup_children.add(imobject)
        group.add(mobject)

    def children_str(self):
        childnames = []
        # for imobject in self.vgroup_children:
        #     childnames.append(mh.getName(imobject))

        return ", ".join(childnames)

    def decl_str(self):
        return f"VGroup({self.children_str()})"

    # def allowed_to_select(self):
    #     return 


class ICircle(IMobject):
    """
    Intermediate Circle class
    """

    def __init__(self, color=RED, radius=None, parent_imobject=None):
        super().__init__(
            Circle(color=color, radius=radius), parent_imobject=parent_imobject
        )
        self.color = color
        self.radius = radius

    def decl_str(self):
        return f'Circle(color="{self.color}", radius={self.radius})'


class ISquare(IMobject):
    """
    Intermediate Square class
    """

    def __init__(self):
        super().__init__(Square())


class IStar(IMobject):
    """
    Intermediate Star class
    """

    def __init__(self):
        super().__init__(Star())


class ITriangle(IMobject):
    """
    Intermediate Triangle class
    """

    def __init__(self):
        super().__init__(Triangle())
