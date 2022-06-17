from PySide6.QtCore import Signal, QObject
import numpy as np
from manim import *
from src.file.writer import Writer
from src.fsm.state import State
from src.intermediate.itree import INode
import src.controllers.mobject_helper as mh


class FsmController(QObject):
    """
    A controller for the finite state machine controller of the animation.
    """

    stateChange = Signal(int, int)
    CLAMP_DISTANCE = 1
    # selectedMobjectChange = Signal(IMobject)
    def __init__(self, scene_controller):
        super().__init__()

        self.num_states = 1
        self.scene_controller = scene_controller

        self.head = State(0)
        self.end = State(2)
        state = State(1)
        self.head.next = state
        state.next = self.end
        state.prev = self.head
        self.end.prev = self.head

        self.is_running = False

        self.curr = state  # animations to play

        self.writer = Writer(self.head, "io/export_scene.py")

    def play_forward(self, fast=True):
        self.curr = self.curr.next
        self.curr.play(self.scene_controller.scene, fast)
        self.stateChange.emit(self.curr.idx, self.num_states)

    def play_back(self):
        self.curr.play_rev(self.scene_controller.scene)
        self.curr = self.curr.prev
        self.stateChange.emit(self.curr.idx, self.num_states)

    def has_loop(self):
        return self.curr.loop is not None and self.curr.loop_cnt > 0

    def run(self):
        self.scene_controller.unselect_mobjects()
        # print("curr", hex(id(self.curr.next)), "end", hex(id(self.end)))
        if self.curr.next == self.end:
            self.set_state_number(1, False)  # go back to start

        self.is_running = True
        while (self.curr.next != self.end or self.has_loop()) and self.is_running:
            if self.has_loop():
                self.curr.loop_cnt -= 1
                self.set_state_number(self.curr.loop[0], False)
            else:
                self.play_forward(fast=False)
            self.stateChange.emit(self.curr.idx, self.num_states)

        self.is_running = False

    def stop(self):
        self.scene_controller.unselect_mobjects()
        self.is_running = False

    def set_state_number(self, idx, userCalled=True):
        if self.is_running:
            return

        if 1 <= idx <= self.num_states:
            if idx < self.curr.idx:
                for _ in range(self.curr.idx, idx, -1):
                    if userCalled and self.curr.loop is not None:
                        self.curr.loop_cnt = self.curr.loop[1]
                    self.play_back()
            else:
                for _ in range(self.curr.idx, idx):
                    self.play_forward()

    def del_state(self):
        if self.is_running or self.num_states <= 1:
            return

        prev = self.curr.prev
        next = self.curr.next
        prev.next = next
        next.prev = prev
        self.curr = prev

        self.num_states -= 1
        self.shift_above_idxs(self.curr.next, -1)

        self.stateChange.emit(self.curr.idx, self.num_states)

    def add_state(self):
        if self.is_running:
            return

        # route new state within the state machine
        new_state = State(self.curr.idx + 1)
        temp = self.curr.next

        self.curr.next = new_state
        new_state.next = temp

        temp.prev = new_state
        new_state.prev = self.curr

        # move to new state
        self.curr = new_state
        self.num_states += 1
        self.shift_above_idxs(self.curr.next, 1)

        # emit signal for widgets
        self.stateChange.emit(self.curr.idx, self.num_states)

    def shift_above_idxs(self, state, inc):
        state.idx = state.prev.idx + inc
        if state != self.end:
            self.shift_above_idxs(state.next, inc)

    def confirm_move(self, mcopy, delta, altdown):
        imobject = mh.get_original(mcopy)
        if imobject is None:
            return  # selected item is old, before transform

        past_point = imobject.past_point

        if (
            not altdown
            and past_point is not None
            and np.linalg.norm(delta) < self.CLAMP_DISTANCE
        ):
            mcopy.move_to(past_point)
            return

        print("confirm move")
        target = mcopy.copy()

        if not isinstance(target, MarkupText):
            target.set_color(self.scene_controller.selected[mcopy])
        self.edit_transform_target(imobject, target, shift=delta)

    def edit_transform_target(
        self, imobject, target, color=None, move_to=None, scale=None, shift=None
    ):
        imobject.edited_at = self.curr.idx  # need to capture after edit

        # -------------

        self.curr.targets[imobject] = target

        if imobject not in self.curr.target_decl_str:
            if not self.created_at_curr_state(imobject):
                self.curr.target_decl_str[imobject] = f"{mh.get_name(imobject)}.copy()"
            else:
                self.curr.target_decl_str[imobject] = imobject.decl_str()

        if color is not None:
            self.curr.called_target_functions[imobject]["set_color"] = {f'"{color}"'}
        if scale is not None:
            if "scale" not in self.curr.rev_attributes[imobject]:
                self.curr.rev_attributes[imobject]["scale"] = imobject.scale
            self.curr.changed_mobject_attributes[imobject]["scale"] = scale
            imobject.scale = scale

            self.curr.called_target_functions[imobject]["scale"] = {str(scale)}
            if scale == 1.0:
                del self.curr.called_target_functions[imobject]["scale"]

        if move_to is not None:
            imobjs = [imobject]
            if not imobject.user_defined and isinstance(imobject.mobject, VGroup):
                imobjs += imobject.vgroup_children

            for imobj in imobjs:
                if "past_point" not in self.curr.rev_attributes[imobj]:
                    self.curr.rev_attributes[imobj]["past_point"] = imobj.past_point
                self.curr.changed_mobject_attributes[imobj]["past_point"] = move_to
                imobj.past_point = move_to
                print("move to edit", imobj, move_to)
                self.curr.called_target_functions[imobj]["move_to"] = {str(move_to)}
        if shift is not None:
            imobjs = [imobject]
            if not imobject.user_defined and isinstance(imobject.mobject, VGroup):
                imobjs += imobject.vgroup_children

            center = mh.get_copy(imobject).get_center().tolist()
            # if isinstance(shift, int) and shift==-1:
            for imobj in imobjs:
                if "past_point" not in self.curr.rev_attributes[imobj]:
                    self.curr.rev_attributes[imobj]["past_point"] = imobj.past_point
                imobj.past_point = center
                print("shift edit", imobj, imobj.past_point)
                self.curr.changed_mobject_attributes[imobj][
                    "past_point"
                ] = imobj.past_point
                self.curr.called_target_functions[imobj]["move_to"] = {
                    str(imobj.past_point)
                }
        # update animation
        if not self.created_at_curr_state(imobject):
            self.curr.add_transform(imobject)
            if imobject not in self.curr.target_decl_str:
                self.curr.target_decl_str[imobject] = f"{mh.get_name(imobject)}.copy()"

    def get_curr_scale(self, imobject):
        res = imobject.past_scale

        # if not self.created_at_curr_state(imobject):
        #     imethod = self.curr.get_apply_function(imobject)
        #     res = (imethod.scale if imethod is not None else 1) or 1

        return res

    def clean_scale(self, scale):
        return (
            scale if scale > 0 else 0.000001
        )  # something small to prevent div zero error

    def created_at_curr_state(self, imobject):
        return imobject.added_state == self.curr

    def created_at_curr_state_with_anim(self, imobject):
        return self.created_at_curr_state(imobject) and imobject.intro_anim is not None

    def instant_add_object_to_curr(self, imobject, select=True, transform=False):
        if isinstance(imobject, INode):
            if imobject.parent_edge is not None:
                self.instant_add_object_to_curr(imobject.parent_edge)
            for child in imobject.vgroup_children:
                self.curr.targets[child] = mh.get_copy(child).copy()
                child.child_add_state = self.curr

        if select:  # if select needs changing
            self.scene_controller.unselect_mobjects()

        if not transform:  # prevents 'self.add' on writer
            self.curr.added.append(imobject)
            self.scene_controller.add_copy(imobject)

        if imobject not in self.curr.targets:
            self.curr.targets[imobject] = imobject.mobject.copy()

        if imobject not in self.curr.target_decl_str:
            self.curr.target_decl_str[imobject] = imobject.decl_str()

        imobject.added_state = self.curr
        imobject.intro_anim = None

        if select and imobject.allowed_to_select:
            self.scene_controller.set_selected_imobject(imobject)

    def instant_remove_obj_at_curr(self, imobject):
        self.scene_controller.remove(imobject)
        if not self.created_at_curr_state(imobject):
            self.curr.removed.append(imobject)
            imobject.removed_state = self.curr
        else:
            imobject.added_state = None
            imobject.is_deleted = True
            mh.remove_copy(mh.get_copy(imobject))
            if imobject in self.curr.added:
                self.curr.added.remove(imobject)
            if imobject in self.curr.targets:
                del self.curr.targets[imobject]

        # remove dependent animations
        if imobject in self.curr.transforms:
            transform = self.curr.transforms[imobject]
            self.curr.animations.remove(transform)
            del self.curr.transforms[imobject]

        if imobject in self.curr.applyfunctions:
            applyfunction = self.curr.applyfunctions[imobject]
            self.curr.animations.remove(applyfunction)
            del self.curr.applyfunctions[imobject]

        if imobject in self.curr.targets:
            del self.curr.targets[imobject]
            del self.curr.target_decl_str[imobject]

        self.scene_controller.unselect_mobjects()

    def add_transform_to_curr(self):
        # TODO: make a transform widget to alter color, position, shape?
        pass

    def export(self, filename="io/export_scene.py"):
        self.writer.initialise(filename=filename)
        self.writer.write()

    def add_python_to_writer(self, file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()

            self.writer.user_defined_text[file_name] = ''.join(lines[1:])
    

