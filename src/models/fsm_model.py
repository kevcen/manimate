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



class StateHandler(QObject):
    stateChange = Signal(int, int)

    def __init__(self, scene_handler):
        super().__init__()

        self.numStates = 1
        self.scene_handler = scene_handler

        self.head = State()
        self.end = State()
        state = State()
        self.head.next = state 
        state.next = self.end 
        state.prev = self.head
        self.end.prev = self.head

        self.is_running = False
        
        self.curr = state # animations to play
        self.currIdx = 1 # curr idx

             
    def playForward(self, fast=True):
        self.currIdx += 1
        self.curr = self.curr.next
        if fast:
            self.scene_handler.playFast(self.curr)
        else:
            self.scene_handler.play(self.curr)

    def playBack(self):
        self.scene_handler.playRev(self.curr)
        self.curr = self.curr.prev 
        self.currIdx -= 1

    def run(self):
        self.scene_handler.unselect_mobjects()
        self.is_running = True
        while self.curr.next != self.end and self.is_running:
            self.stateChange.emit(self.currIdx + 1, self.numStates)
            self.playForward(fast=False)
            
        self.is_running = False

    def stop(self):
        self.scene_handler.unselect_mobjects()
        self.is_running = False

    def set_state_number(self, idx):
        if 1 <= idx <= self.numStates:
            if idx < self.currIdx:
                for _ in range(self.currIdx, idx, -1):
                    self.playBack()
            else:
                for _ in range(self.currIdx, idx):
                    self.playForward()

    def add_state(self):
        if self.is_running:
            return 

        #route new state within the state machine
        new_state = State()
        temp = self.curr.next 

        self.curr.next = new_state
        new_state.next = temp 

        temp.prev = new_state
        new_state.prev = self.curr 

        #move to new state
        self.curr = new_state
        self.numStates += 1
        self.currIdx += 1

        #emit signal for widgets
        self.stateChange.emit(self.currIdx, self.numStates)
        
    def confirm_move(self, mcopy, point):
        imobject = mh.getOriginal(mcopy)

        target = mcopy.copy()
        target.set_color(self.scene_handler.selected[mcopy])


        # update animation
        if not self.created_at_curr_state(imobject):
            self.curr.targets[imobject] = target 
            self.curr.changedTargetAttributes[imobject]['move_to'] = str(point.tolist())
        else:
            imobject.mobject = target


    def capture_prev(self, mcopy):
        # capture previous frame for reverse if editable
        if mcopy not in self.curr.prev.targets.inverse:
            imobject = mh.getOriginal(mcopy)
            if imobject not in self.curr.prev.targets:
                target = mcopy.copy()
                target.set_color(self.scene_handler.selected[mcopy])
                # self.curr.prev.targets[imobject] = target
                self.curr.rev_targets[imobject] = target

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
        self.scene_handler.playCopy(create, self.curr)

    def instant_add(self, mobject):
        # TODO: remove after line to connect nodes uses imobject
        self.curr.added.add(mobject)
        self.scene_handler.add(mobject)

    def instant_add_object_to_curr(self, imobject):
        self.curr.added.add(imobject)
        self.scene_handler.add(imobject)

        imobject.addedState = self.curr
        imobject.introAnim = None

    def instant_remove_obj_at_curr(self, imobject):
        self.scene_handler.remove(imobject)
        if imobject.addedState != self.curr:
            self.curr.removed.add(imobject)
            imobject.removedState = self.curr
        else:
            imobject.addedState = None 
            self.curr.added.remove(imobject)


    def add_transform_to_curr(self):
        # TODO: make a transform widget to alter color, position, shape?
        pass

    def export(self):
        writer = Writer(self.head, "io/export_scene.py")

        writer.write()

