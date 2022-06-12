from intermediate.ianimation import ITransform
from intermediate.imobject import ICircle, IDependent, IMobject
from intermediate.itext import IText
import controllers.mobject_helper as mh
from manim import *


class INode(IMobject):
    """
    Intermediate mobject representing a single Tree Node
    """

    def __init__(self, fsm_controller, text="t"):
        self.parent = None
        self.children = []

        # Manim mobjects
        self.text = text
        self.label = IText(self.text, parent_imobject=self)
        self.label.is_deleted = True  # do not print
        self.container = ICircle(radius=0.6, color=RED, parent_imobject=self)
        self.container.is_deleted = True  # do not print
        self.mobject = VGroup(self.label.mobject, self.container.mobject)
        self.mobject.set_color(RED)
        self.parent_edge = None
        self.vgroup_children = [self.label, self.container]

        # Aux info
        self.fsm_controller = fsm_controller
        self.fsm_controller.curr.target_decl_str[
            self.label
        ] = f"{mh.get_name(self)}.label"
        self.fsm_controller.curr.target_decl_str[
            self.container
        ] = f"{mh.get_name(self)}.container"
        for child in self.vgroup_children:
            self.fsm_controller.curr.targets[child] = child.mobject.copy()
            child.child_add_state = self.fsm_controller.curr
            child.past_point = [0, 0, 0]

        super().__init__(self.mobject)

    def spawn_child(self):
        child = INode(self.fsm_controller)
        parentcpy = mh.get_copy(self)
        self.add_edge(self, child)
        self.children.append(child)

        child.show_node()

        new_point = [parentcpy.get_x(), parentcpy.get_y() - 2, 0]
        mh.get_copy(child).move_to(np.array(new_point))
        child.past_point = new_point
        self.fsm_controller.curr.targets[child] = mh.get_copy(child).copy()
        # self.fsm_controller.curr.targets[child].set_color()
        self.fsm_controller.curr.target_decl_str[child] = child.decl_str()
        self.fsm_controller.curr.called_target_functions[child]["move_to"] = [
            str(new_point)
        ]
        for vgroup_child in child.vgroup_children:
            vgroup_child.past_point = mh.get_copy(vgroup_child).get_center().tolist()
            print("spawn", vgroup_child, vgroup_child.past_point)
            self.fsm_controller.curr.called_target_functions[vgroup_child][
                "move_to"
            ] = [str(vgroup_child.past_point)]

    def show_node(self):
        if self.parent_edge is not None:
            self.fsm_controller.instant_add_object_to_curr(self.parent_edge)
        self.fsm_controller.instant_add_object_to_curr(self)

    def align_children(self):
        camera = self.fsm_controller.scene_controller.renderer.camera
        fw, fh = camera.frame_shape
        fsx = camera.get_center()[0] - fw / 2

        depth = self.align_children_x(fw, fsx)
        sy = mh.get_copy(self).get_y()
        height_below_self = sy - (camera.get_center()[1] - fh / 2)
        self.align_children_y(height_below_self / depth, sy, 1)

        ## TODO: movement store for writer

    def align_children_x(self, fw, fs):
        if not self.children:
            return 1
        n = len(self.children)
        interval = fw / n
        depth = 1
        for i in range(n):
            mobject = mh.get_copy(self.children[i])
            y = mobject.get_y()
            x = fs + interval / 2 + i * interval
            mobject.move_to([x, y, 0])
            depth = max(
                depth,
                1 + self.children[i].align_children_x(interval, fs + i * interval),
            )

        return depth

    def align_children_y(self, dy, sy, depth):
        if not self.children:
            return

        for child in self.children:
            mobject = mh.get_copy(child)
            current_x = mobject.get_x()
            y = sy - dy * depth
            mobject.move_to([current_x, y, 0])
            self.fsm_controller.edit_transform_target(
                child, mobject.copy(), shift=-1
            )  # track current position
            # for vgroup_child in child.vgroup_children:
            #     # self.fsm_controller.curr.called_target_functions[vgroup_child]["move_to"] = [
            #     #     str(vgroup_child.past_point)
            #     # ]
            #     target = mh.get_copy(vgroup_child).copy()
            #     if vgroup_child in self.fsm_controller.scene_controller.selected:
            #         target.set_color(self.fsm_controller.scene_controller.selected[mh.get_copy(child)])
            #     self.fsm_controller.edit_transform_target(
            #         vgroup_child, target, move_to=[current_x, y, 0]
            # )
            child.align_children_y(dy, sy, depth + 1)

    def change_label_text(self, new_text_str):
        curr_state = self.fsm_controller.curr
        self.label.is_deleted = False  # do print
        # print('text change')
        # mh.get_copy(self.label).set_color(RED)
        # return

        # print("curr text", self.text)
        # create new text
        new_text = Text(new_text_str)
        color = self.fsm_controller.scene_controller.selected[mh.get_copy(self)]
        print(mh.get_copy(self).get_color())
        new_text.match_color(mh.get_copy(self))  # selected colour
        center_point = mh.get_copy(self).get_center().tolist()
        new_text.move_to(center_point)
        new_text.scale(self.past_scale)

        print("LABEL CHANGE", self.label, self.label.past_point)
        # configure transforms
        self.fsm_controller.curr.capture_prev(mh.get_copy(self.label))
        curr_state.targets[self.label] = new_text.copy()
        if self.label.child_add_state == curr_state:
            curr_state.target_decl_str[self.label] = f"{mh.get_name(self)}.label"
        else:
            curr_state.target_decl_str[self.label] = f'Text("{new_text_str}")'

        self.edited_at = curr_state.idx
        if not self.fsm_controller.created_at_curr_state(self):
            curr_state.add_transform(self.label)

        if "text" not in curr_state.rev_attributes[self]:
            curr_state.changed_mobject_attributes[self]["text"] = self.text
        self.text = new_text_str
        curr_state.rev_attributes[self]["text"] = self.text
        # setup current ui

        curr_state.play_copy(
            ITransform(self.label), self.fsm_controller.scene_controller.scene
        )

        # mh.get_copy(self).add(mh.get_copy(self.label))
        # mh.setCopy(self, self.mobject)

        # store for writer
        curr_state.targets[self] = mh.get_copy(self).copy()
        curr_state.targets[self].set_color(color)
        curr_state.targets[self.label].set_color(color)
        self.fsm_controller.curr.called_target_functions[self.label]["move_to"] = [
            str(center_point)
        ]
        print("LABEL CHANGE AFTER", self.label.past_point)

        if not self.fsm_controller.created_at_curr_state(
            self
        ):  # match properties with old label
            self.fsm_controller.curr.called_target_functions[self.label][
                "match_color"
            ] = [self]

            ## can be placed outside if statement too
            self.fsm_controller.curr.called_target_functions[self.label]["scale"] = {
                str(self.past_scale)
            }
            if self.past_scale == 1.0:
                del self.fsm_controller.curr.called_target_functions[self.label]["scale"]

            if self not in curr_state.target_decl_str:
                curr_state.target_decl_str[self] = f"{mh.get_name(self)}.copy()"

        else:
            curr_state.target_decl_str[self] = self.decl_str()

        # mh.get_copy(self.label).set_color('#e622c5')

    def change_parent(self, new_parent):
        # TODO: needs to put the parent at a higher target
        if "parent" not in self.fsm_controller.curr.rev_attributes[self]:
            self.fsm_controller.curr.rev_attributes[self]["parent"] = self.parent
        self.fsm_controller.curr.changed_mobject_attributes[self]["parent"] = new_parent
        self.fsm_controller.curr.called_target_functions[self]["set_parent"] = [
            new_parent
        ]

        if new_parent is None:
            self.fsm_controller.instant_remove_obj_at_curr(self.parent_edge)
            self.parent_edge = None
        elif self.parent is None:
            self.add_edge(new_parent, self)
            self.fsm_controller.instant_add_object_to_curr(self.parent_edge)

        self.parent = new_parent
        # parent edge should auto update through updater

    def add_edge(self, parent, child):
        child.parent = parent
        child.parent_edge = IParentEdge(child)
        child.parent_edge.continuously_update()

    def decl_str(self):
        return f"Tree(\"{self.text}\", parent={mh.get_name(self.parent) if self.parent is not None else 'None'})"  # Text will be altered with target


class IParentEdge(IDependent):
    """
    Intermediate mobject representing an edge connecting a node to its a parent
    """

    def __init__(self, node):
        self.node = node
        # Move connecting line
        pn = node.parent.mobject
        cn = node.mobject
        self.mobject = Line(pn.get_bottom(), cn.get_top(), color=RED)

        super().__init__(self.mobject)
        self.allowed_to_select = False

    def continuously_update(self):
        self.mobject.add_updater(lambda mob: self.update_line(mob))

    def update_line(self, line):
        if self.node.parent is None:
            return

        line.put_start_and_end_on(
            mh.get_copy(self.node.parent).get_bottom(), mh.get_copy(self.node).get_top()
        )

    def decl_str(self):
        return f"ParentEdge({mh.get_name(self.node)})"
