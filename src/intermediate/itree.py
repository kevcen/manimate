from intermediate.imobject import IMobject
from manim import *
import models.mobject_helper as mh

class INode(IMobject):
    def __init__(self, state_handler):
        self.parent = None
        self.children = []

        # Manim mobjects
        self.label = Text("t") 
        self.label.set_color(RED)
        self.container = Circle(radius=0.6, color=RED)
        self.mobject = VGroup(self.label, self.container, color=RED)
        self.parent_edge = None

        # Aux info
        self.state_handler = state_handler

    def child(self):
        child = INode(self.state_handler)
        parentcpy = mh.getCopy(self)
        child.mobject.move_to(np.array([parentcpy.get_x(), parentcpy.get_y() - 2, 0]))
        child.parent = self 
        child.parent_edge = IParentEdge(child)
        child.parent_edge.continuously_update()
        return child

    def spawn_child(self):
        child = self.child()
        self.children.append(child)
        child.show_node()

    def show_node(self):
        self.state_handler.instant_add_object_to_curr(self)
        if self.parent_edge is not None:
            self.state_handler.instant_add_object_to_curr(self.parent_edge)

    def change_parent(self, parent):
        self.parent = parent
        #parent edge should auto update through updater


class IParentEdge(IMobject):
    def __init__(self, node):
        print(node)
        self.node = node

        # Move connecting line
        pn = node.parent.mobject
        cn = node.mobject

        self.mobject = Line(pn.get_bottom(),
                        cn.get_top(), color=RED)

    def continuously_update(self):
        self.mobject.add_updater(lambda mob: mob.put_start_and_end_on(mh.getCopy(self.node.parent).get_bottom(),
                    mh.getCopy(self.node).get_top()))

    