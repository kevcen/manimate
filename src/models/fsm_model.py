import sys
from PySide6.QtCore import (Signal, QObject)
from file.writer import Writer
from fsm.state import State
from manim import *
import time
from intermediate.ianimation import ICreate
from models import scene_model
import numpy as np
import models.mobject_helper as mh



class FsmModel(QObject):
    stateChange = Signal(int, int)

    def __init__(self, scene_model):
        super().__init__()

        self.numStates = 1
        self.scene_model = scene_model

        self.head = State(None)
        self.end = State(None)
        state = State(1)
        self.head.next = state 
        state.next = self.end 
        state.prev = self.head
        self.end.prev = self.head

        self.is_running = False
        
        self.curr = state # animations to play
             
    def playForward(self, fast=True):
        self.curr = self.curr.next
        if fast:
            self.scene_model.playFast(self.curr)
        else:
            self.scene_model.play(self.curr)

    def playBack(self):
        self.scene_model.playRev(self.curr)
        self.curr = self.curr.prev 

    def run(self):
        self.scene_model.unselect_mobjects()
        self.is_running = True
        while self.curr.next != self.end and self.is_running:
            self.playForward(fast=False)
            self.stateChange.emit(self.curr.idx, self.numStates)
            
        self.is_running = False

    def stop(self):
        self.scene_model.unselect_mobjects()
        self.is_running = False

    def set_state_number(self, idx):
        if 1 <= idx <= self.numStates:
            if idx < self.curr.idx:
                for _ in range(self.curr.idx, idx, -1):
                    self.playBack()
            else:
                for _ in range(self.curr.idx, idx):
                    self.playForward()

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
        self.shift_above_idxs(self.curr.next)

        #emit signal for widgets
        self.stateChange.emit(self.curr.idx, self.numStates)
    
    def shift_above_idxs(self, state):
        if state == self.end:
            return 

        state.idx = state.prev.idx + 1
        self.shift_above_idxs(state.next)
        
    def confirm_move(self, mcopy, point):
        imobject = mh.getOriginal(mcopy)
        if imobject is None:
            return #selected item is old, before transform 
            
        imobject.editedAt = self.curr.idx #need to capture after edit

        # Circle().get_center()
        past_mobject = None 
        if imobject not in self.curr.targets:
            print('imobject mobj')
            past_mobject = imobject.mobject 
        else:
            print('targets mobj')
            past_mobject = self.curr.targets[imobject]

        print('conf move', past_mobject.get_center(), mcopy.get_center())
        print(past_mobject, mcopy)
        if (past_mobject.get_center() == mcopy.get_center()).all():
            return
            
        target = mcopy.copy()
        if not isinstance(target, MarkupText):
            target.set_color(self.scene_model.selected[mcopy])

        # update animation
        if not self.created_at_curr_state(imobject):
            self.curr.targets[imobject] = target
            self.curr.changedTargetAttributes[imobject]['move_to'] = str(point.tolist())

            self.curr.addTransform(imobject)
        else:
            print('new object no transform')
            self.curr.targets[imobject] = target
            imobject.mobject = target

    def created_at_curr_state(self, imobject):
        return imobject.addedState == self.curr

    def created_at_curr_state_with_anim(self, imobject):
        return self.created_at_curr_state(imobject) and imobject.introAnim is not None

    def add_object_to_curr(self, imobject):
        # TODO: make it instant with scene.add
        create = ICreate(imobject)
        self.curr.animations.append(create)
        self.curr.targets[imobject] = imobject.mobject
        imobject.addedState = self.curr
        imobject.introAnim = create
        # self.curr.prev.added.add(imobject)
        self.scene_model.playCopy(create, self.curr)


    def instant_add_object_to_curr(self, imobject):
        self.curr.added.add(imobject)
        self.curr.targets[imobject] = imobject.mobject
        self.scene_model.addCopy(imobject)

        imobject.addedState = self.curr
        imobject.introAnim = None

    def instant_remove_obj_at_curr(self, imobject):
        self.scene_model.remove(imobject)
        if not self.created_at_curr_state(imobject):
            print('removed at this state')
            self.curr.removed.add(imobject)
            imobject.removedState = self.curr
        else:
            print('fully disappeared')
            imobject.addedState = None
            mh.removeCopy(mh.getCopy(imobject))
            if imobject in self.curr.added:
                self.curr.added.remove(imobject)
            
            

        if imobject in self.curr.transforms:
            transform = self.curr.transforms[imobject]
            self.curr.animations.remove(transform)
            del self.curr.transforms[imobject]
        if imobject in self.curr.targets:
            del self.curr.targets[imobject]

        print(len(self.curr.animations))



    def add_transform_to_curr(self):
        # TODO: make a transform widget to alter color, position, shape?
        pass

    def export(self):
        writer = Writer(self.head, "io/export_scene.py")

        writer.write()

