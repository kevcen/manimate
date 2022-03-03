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

             
    def playCurr(self, fast=True):
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
            self.playCurr(False)
            self.stateChange.emit(self.currIdx, self.numStates)
            
        self.is_running = False

    def stop(self):
        self.is_running = False

    def set_state_number(self, idx):
        if 0 <= idx <= self.numStates:
            if idx < self.currIdx:
                for _ in range(self.currIdx, idx, -1):
                    self.playBack()
            else:
                for _ in range(self.currIdx, idx):
                    self.playCurr()


    def add_object(self, mobject):
        # self.curr.mobjects.append(mobject)
        create = Create(mobject)
        self.curr.prev.animations.append(create)
        self.curr.targets[mobject] = mobject
        self.scene_handler.playCopy(create, self.curr.prev)
        # self.scene_handler.replay(self.curr)
        # self.scene_handler.add(mobject)

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
        # # mobject = self.curr.prev.targets.inverse[mcopy]
        # if mobject not in self.curr.targets:
        #     transform = Transform(mobject, target)
        #     # self.curr.targets[mcopy] = mobject
        #     # self.curr.prev.targets[mobject] = mobject.copy()
        #     self.curr.prev.animations.append(transform)

        #     replace = Transform(mobject, target)
        #     self.scene_handler.playOne(replace, self.curr.prev)
        #     # self.scene_handler.replay(self.curr)



        # mcopy.set_color(GREEN_C)
        # # mobject = self.mobject_handler.getOriginal(mcopy) #nvm gets target
        # tobject = self.mobject_handler.getOriginal(mcopy) #inner representation
        # mobject = self.curr.targets.inverse[tobject]

        # target = mcopy.copy() #capture position
        # target.set_color(GREEN_C)

        # # oldTarget = self.curr.targets[mobject] # is the same as mcopy
        # oldTarget = mcopy
        # self.curr.targets[mobject] = target


        # # update animation
        # replace = self.curr.prev.transforms[mobject]
        # replace.target_mobject = target

        # replace2 = Transform(oldTarget, target) #replace copies on screen
        # self.scene_handler.playCopy(replace2, self.curr.prev)

        # if self.scene_handler.selected == mcopy:
        #     self.scene_handler.selected = self.mobject_handler.getCopy(target)

        mobject = self.mobject_handler.getOriginal(mcopy)

        target = mcopy.copy()
        self.curr.targets[mobject] = target 

        # update animation
        replace = self.curr.prev.getTransform(mobject)
        replace.target_mobject = target






    def select_mobject(self, mcopy):
        if mcopy in self.curr.prev.targets.inverse: #already copied for this frame
            return 

        mobject = self.mobject_handler.getOriginal(mcopy)
        self.curr.prev.targets[mobject] = mcopy.copy() #capture previous frame for reverse 
        
        # # mobject = self.curr.prev.targets.inverse[mcopy]
        # mobject = self.mobject_handler.getOriginal(mcopy)
        # #preserve previous state if current frame changes it
        # # self.curr.prev.targets[mobject] = mcopy.copy()
        # target = mcopy.copy() #capture position
        # self.curr.targets[mobject] = target


        # replace = Transform(mobject, target)
        # self.curr.prev.transforms[mobject] = replace

        # self.curr.prev.animations.append(replace)
        # self.scene_handler.playCopy(replace, self.curr.prev)


        # if self.scene_handler.selected == mcopy:
        #     self.scene_handler.selected = self.mobject_handler.getCopy(target)


    def create_target(self, mobject):
        # target = mobject.copy()
        pass

    def add_transform(self):
        pass


