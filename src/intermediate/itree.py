from intermediate.ianimation import ITransform
from intermediate.imobject import ICircle, IMobject
from manim import *
from intermediate.itext import IText
import models.mobject_helper as mh

class INode(IMobject):
    def __init__(self, fsm_model):
        self.parent = None
        self.children = []

        # Manim mobjects
        self.text = "t"
        self.label = IText(self.text, parentImobject=self)
        self.container = ICircle(radius=0.6, color=RED, parentImobject=self)
        self.mobject = VGroup(self.label.mobject, self.container.mobject)
        self.mobject.set_color(RED)
        self.parent_edge = None
        self.vgroup_children = [self.label, self.container]
        # TODO: fadein/create parent edge too when node has intro anim

        # Aux info
        self.fsm_model = fsm_model

        super().__init__(self.mobject)

    def spawn_child(self):
        child = INode(self.fsm_model)
        parentcpy = mh.getCopy(self)
        child.mobject.move_to(np.array([parentcpy.get_x(), parentcpy.get_y() - 2, 0]))
        self.fsm_model.curr.targets[child] = child.mobject.copy()
        self.fsm_model.curr.targetDeclStr[child] = child.declStr()
        self.fsm_model.curr.calledTargetFunctions[child]['move_to'] = [str([parentcpy.get_x(), parentcpy.get_y() - 2, 0])]
        self.add_edge(self, child)
        self.children.append(child)
        child.show_node()

    def show_node(self):
        self.fsm_model.instant_add_object_to_curr(self)
        if self.parent_edge is not None:
            self.fsm_model.instant_add_object_to_curr(self.parent_edge)

    def change_label_text(self, new_text_str):
        curr_state = self.fsm_model.curr

        # create new text
        new_text = Text(new_text_str)
        new_text.match_color(mh.getCopy(self.label))
        new_text.move_to(mh.getCopy(self.label).get_center())

        # configure transforms
        self.fsm_model.curr.capture_prev(mh.getCopy(self.label))
        curr_state.targets[self.label] = new_text
        if not self.fsm_model.created_at_curr_state(self):
            curr_state.addTransform(self.label)

        #store for writer 
        self.text = new_text
        curr_state.targetDeclStr[self] = self.declStr()
        if not self.fsm_model.created_at_curr_state(self):
            self.fsm_model.curr.calledTargetFunctions[self.label]['match_color'] = [self.label]
            self.fsm_model.curr.calledTargetFunctions[self.label]['move_to'] = [str(mh.getCopy(self.label).get_center().tolist())]

        # setup current ui
        curr_state.playCopy(ITransform(self.label), self.fsm_model.scene_model.scene)
        
        mh.getCopy(self).add(mh.getCopy(self.label))
        # mh.setCopy(self, self.mobject)



    def change_parent(self, new_parent):
        self.fsm_model.curr.revAttributes[self]['parent'] = self.parent
        self.fsm_model.curr.changedMobjectAttributes[self]['parent'] = new_parent

        if new_parent is None:
            self.fsm_model.instant_remove_obj_at_curr(self.parent_edge)
            self.parent_edge = None
        elif self.parent is None:
            self.add_edge(new_parent, self)
            self.fsm_model.instant_add_object_to_curr(self.parent_edge)
        
        self.parent = new_parent
        #parent edge should auto update through updater

    def add_edge(self, parent, child):
        child.parent = parent 
        child.parent_edge = IParentEdge(child)
        child.parent_edge.continuously_update()

    def declStr(self):
        return f"Tree(\"{self.text}\", parent={mh.getName(self.parent) if self.parent is not None else 'None'})" # Text will be altered with target


class IParentEdge(IMobject):
    def __init__(self, node):
        self.node = node
        # Move connecting line
        pn = node.parent.mobject
        cn = node.mobject
        self.mobject = Line(pn.get_bottom(),
                        cn.get_top(), color=RED)

        super().__init__(self.mobject)
        self.allowed_to_select = False

    def continuously_update(self):
        self.mobject.add_updater(lambda mob: self.updateLine(mob))

    def updateLine(self, line):
        if self.node.parent is None:
            return 

        line.put_start_and_end_on(mh.getCopy(self.node.parent).get_bottom(),
                    mh.getCopy(self.node).get_top())


    def declStr(self):
        return f"ParentEdge({mh.getName(self.node)})"

    