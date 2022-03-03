import sys
from PySide6.QtCore import (Signal, QObject)
from fsm.state import State
from manim import *
import time
from model import scene_handler



class StateHandler(QObject):
    stateChange = Signal(int, int)

    def __init__(self, scene_handler, mobject_handler):
        super().__init__()

        self.numStates = 1
        self.scene_handler = scene_handler
        self.mobject_handler = mobject_handler

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
        if fast:
            self.scene_handler.playFast(self.curr)
        else:
            self.scene_handler.play(self.curr)
        self.currIdx += 1
        self.curr = self.curr.next

    def playBack(self):
        self.curr = self.curr.prev 
        self.currIdx -= 1
        self.scene_handler.playRev(self.curr)

    def run(self):
        self.is_running = True
        while self.curr.next != self.end and self.is_running:
            self.playForward(fast=False)
            self.stateChange.emit(self.currIdx, self.numStates)
            
        self.is_running = False

    def stop(self):
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

        new_state = State()
        temp = self.curr.next 

        self.curr.next = new_state
        new_state.next = temp 

        temp.prev = new_state
        new_state.prev = self.curr 

        self.curr = new_state
        self.numStates += 1
        self.currIdx += 1

        self.stateChange.emit(self.currIdx, self.numStates)
        
    def move_to_target(self, mcopy):
        mobject = self.mobject_handler.getOriginal(mcopy)

        target = mcopy.copy()
        self.curr.targets[mobject] = target 

        # update animation
        replace = self.curr.prev.getTransform(mobject)
        replace.target_mobject = target

    def select_mobject(self, mcopy):
        #capture previous frame for reverse 
        if mcopy not in self.curr.prev.targets.inverse:
            mobject = self.mobject_handler.getOriginal(mcopy)
            self.curr.prev.targets[mobject] = mcopy.copy()

    def created_here(self, mobject):
        return mobject in self.curr.targets and self.curr.targets[mobject] == mobject

    def add_object(self, mobject):
        # TODO: make it instant with scene.add

        create = Create(mobject)
        self.curr.prev.animations.append(create)
        self.curr.targets[mobject] = mobject

        self.scene_handler.playCopy(create, self.curr.prev)

    def add_transform(self):
        # TODO: make a transform widget to alter color, position, shape?
        pass


