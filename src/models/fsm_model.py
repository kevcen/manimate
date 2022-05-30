import sys
from PySide6.QtCore import (Signal, QObject)
from file.writer import Writer
from fsm.state import State
from manim import *
import time
from intermediate.ianimation import ICreate
from intermediate.imobject import IMobject
from models import scene_model
import numpy as np
import models.mobject_helper as mh



class FsmModel(QObject):
    stateChange = Signal(int, int)
    CLAMP_DISTANCE = 1
    # selectedMobjectChange = Signal(IMobject)
    def __init__(self, scene_model):
        super().__init__()

        self.numStates = 1
        self.scene_model = scene_model

        self.head = State(0)
        self.end = State(2)
        state = State(1)
        self.head.next = state 
        state.next = self.end 
        state.prev = self.head
        self.end.prev = self.head

        self.is_running = False
        
        self.curr = state # animations to play
             
    def playForward(self, fast=True):
        self.curr = self.curr.next
        self.curr.play(self.scene_model.scene, fast)

    def playBack(self):
        self.curr.playRev(self.scene_model.scene)
        self.curr = self.curr.prev 

    def hasLoop(self):
        return self.curr.loop is not None and self.curr.loopCnt > 0

    def run(self):
        self.scene_model.unselect_mobjects()
        self.is_running = True
        if self.curr.next == self.end:
            self.set_state_number(1, False) #go back to start

        while (self.curr.next != self.end or self.hasLoop()) and self.is_running:
            print(self.curr.idx)
            if self.hasLoop():
                self.curr.loopCnt -= 1
                self.set_state_number(self.curr.loop[0], False)
                # TODO: reverse all the stuff
            else:
                self.playForward(fast=False)
            self.stateChange.emit(self.curr.idx, self.numStates)
            
        self.is_running = False

    def stop(self):
        self.scene_model.unselect_mobjects()
        self.is_running = False

    def set_state_number(self, idx, userCalled=True):
        print('SET STATE NUMBER?', idx, self.curr.idx)
        if 1 <= idx <= self.numStates:
            if idx < self.curr.idx:
                for _ in range(self.curr.idx, idx, -1):
                    if userCalled and self.curr.loop is not None:
                        self.curr.loopCnt = self.curr.loop[1]
                    # print('move back')
                    self.playBack()
            else:
                for _ in range(self.curr.idx, idx):
                    self.playForward()

    def del_state(self):
        if self.is_running or self.numStates <= 1:
            return

        prev = self.curr.prev
        next = self.curr.next
        prev.next = next
        next.prev = prev
        self.curr = prev

        self.numStates -= 1
        self.shift_above_idxs(self.curr.next, -1)

        self.stateChange.emit(self.curr.idx, self.numStates)

    def add_state(self):
        # print('idx before', self.curr.idx)
        # print(hex(id(self.curr)))
        if self.is_running:
            return 

        #route new state within the state machine
        new_state = State(self.curr.idx + 1)
        temp = self.curr.next 

        self.curr.next = new_state
        new_state.next = temp 

        temp.prev = new_state
        new_state.prev = self.curr 

        #move to new state
        self.curr = new_state
        # print('index is now', self.curr.idx)
        # print(hex(id(self.curr)))
        self.numStates += 1
        self.shift_above_idxs(self.curr.next, 1)

        #emit signal for widgets
        self.stateChange.emit(self.curr.idx, self.numStates)
    
    def shift_above_idxs(self, state, inc):
        state.idx = state.prev.idx + inc
        if state != self.end:
            self.shift_above_idxs(state.next, inc)
        
    def confirm_move(self, mcopy, point):
        imobject = mh.getOriginal(mcopy)
        if imobject is None:
            return #selected item is old, before transform 

        past_point = imobject.move_to

        if past_point is not None and np.linalg.norm(past_point-point) < self.CLAMP_DISTANCE:
            mcopy.move_to(past_point)
            return

        target = mcopy.copy()

        if not isinstance(target, MarkupText):
            target.set_color(self.scene_model.selected[mcopy])
        self.edit_transform_target(imobject, target, move_to=point)

    def edit_transform_target(self, imobject, target, color=None, move_to=None, scale=None):
        imobject.editedAt = self.curr.idx #need to capture after edit

        #-------------

        self.curr.targets[imobject] = target
        self.curr.targetDeclStr[imobject] = imobject.declStr()  

        if color is not None:
            self.curr.calledTargetFunctions[imobject]['set_color'] = {f"\"{color}\""}
        if scale is not None:
            imobject.scale = scale # used for tracking old scale to do a proportionate scaling
            self.curr.calledTargetFunctions[imobject]['scale'] = {str(scale)}
        if move_to is not None:
            imobject.move_to = move_to
            self.curr.calledTargetFunctions[imobject]['move_to'] = {str(move_to.tolist())}

        # update animation
        if not self.created_at_curr_state(imobject):
            # self.curr.targets[imobject] = target
            self.curr.addTransform(imobject)
            self.curr.targetDeclStr[imobject] = f"{mh.getName(imobject)}.copy()"

            # if move_to is not None:
            #     imethod.move_to = move_to
            
            # if color is not None:
            #     imethod.color = color
            # if scale is not None:
            #     imethod.scale = scale
        # else:



    def get_curr_scale(self, imobject):
        res = imobject.scale
        
        # if not self.created_at_curr_state(imobject):
        #     imethod = self.curr.getApplyFunction(imobject)
        #     res = (imethod.scale if imethod is not None else 1) or 1
        
        return res
    
    def clean_scale(self, scale):
        return scale if scale > 0 else 0.000001 #something small to prevent div zero error

    def created_at_curr_state(self, imobject):
        return imobject.addedState == self.curr

    def created_at_curr_state_with_anim(self, imobject):
        return self.created_at_curr_state(imobject) and imobject.introAnim is not None

    def instant_add_object_to_curr(self, imobject, select=True):
            
        self.curr.added.add(imobject)
        self.curr.targets[imobject] = imobject.mobject
        self.curr.targetDeclStr[imobject] = imobject.declStr()
        self.scene_model.addCopy(imobject)

        imobject.addedState = self.curr
        imobject.introAnim = None

        if select and imobject.allowed_to_select:
            self.scene_model.set_selected_imobject(imobject)

    def instant_remove_obj_at_curr(self, imobject):
        self.scene_model.remove(imobject)
        if not self.created_at_curr_state(imobject):
            self.curr.removed.add(imobject)
            imobject.removedState = self.curr
        else:
            imobject.addedState = None
            mh.removeCopy(mh.getCopy(imobject))
            if imobject in self.curr.added:
                self.curr.added.remove(imobject)     
        
        #remove dependent animations
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
            del self.curr.targetDeclStr[imobject]

        self.scene_model.unselect_mobjects()



    def add_transform_to_curr(self):
        # TODO: make a transform widget to alter color, position, shape?
        pass

    def export(self):
        writer = Writer(self.head, "io/export_scene.py")

        writer.write()

