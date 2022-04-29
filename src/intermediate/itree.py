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
        # TODO: fadein/create parent edge too when node has intro anim

        # Aux info
        self.state_handler = state_handler

        super().__init__(self.mobject)

    def child(self):
        child = INode(self.state_handler)
        parentcpy = mh.getCopy(self)
        child.mobject.move_to(np.array([parentcpy.get_x(), parentcpy.get_y() - 2, 0]))
        self.add_edge(self, child)
        return child

    def spawn_child(self):
        child = self.child()
        self.children.append(child)
        child.show_node()

    def show_node(self):
        self.state_handler.instant_add_object_to_curr(self)
        if self.parent_edge is not None:
            self.state_handler.instant_add_object_to_curr(self.parent_edge)

    def change_parent(self, new_parent):
        self.state_handler.curr.revAttributes[self]['parent'] = self.parent
        self.state_handler.curr.changedMobjectAttributes[self]['parent'] = new_parent
        
        if new_parent is None:
            self.state_handler.instant_remove_obj_at_curr(self.parent_edge)
            self.parent_edge = None
        elif self.parent is None:
            self.add_edge(new_parent, self)
            self.state_handler.instant_add_object_to_curr(self.parent_edge)
        
        self.parent = new_parent
        #parent edge should auto update through updater

    def add_edge(self, parent, child):
        parentcpy = mh.getCopy(parent)
        child.parent = parent 
        child.parent_edge = IParentEdge(child)
        child.parent_edge.continuously_update()


    def copyWith(self, mobject):
        node = INode(self.state_handler)
        node.mobject = mobject 
        return node


class IParentEdge(IMobject):
    def __init__(self, node):
        self.node = node
        # Move connecting line
        pn = node.parent.mobject
        cn = node.mobject
        self.mobject = Line(pn.get_bottom(),
                        cn.get_top(), color=RED)

        super().__init__(self.mobject)
        self.movable = False



        

    def continuously_update(self):
        self.mobject.add_updater(lambda mob: self.updateLine(mob))

    def updateLine(self, line):
        if self.node.parent is None:
            return 

        line.put_start_and_end_on(mh.getCopy(self.node.parent).get_bottom(),
                    mh.getCopy(self.node).get_top())


    