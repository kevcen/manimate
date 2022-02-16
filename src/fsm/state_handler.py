import sys
from PySide6.QtCore import (Signal, QObject)
from fsm.state import State
from manim import *
import time



class StateHandler(QObject):
    stateChange = Signal(int)

    def __init__(self, scene_handler):
        super().__init__()

        self.numStates = 2
        self.scene_handler = scene_handler
        c1 = Circle()
        s1 = Square()
        state1 = State([Create(c1)])
        state2 = State([ReplacementTransform(c1, s1)])
        state3 = State([])
        state1.next = state2 
        state2.prev = state1
        state2.next = state3
        state3.prev = state2

        self.head = state1
        self.end = state3

        self.is_running = False
        
        self.curr = self.head
        self.currIdx = 0
         
    def playCurr(self, fast=True):
        self.currIdx += 1
        if fast:
            self.scene_handler.playFast(self.curr)
        else:
            self.scene_handler.play(self.curr)
        # self.playCurr()
        self.curr = self.curr.next

    def playBack(self):
        self.currIdx -= 1
        self.curr = self.curr.prev 
        self.scene_handler.playRev(self.curr)

    def run(self):
        # self.is_running = True
        while self.curr != self.end:
            self.playCurr(False)
            self.stateChange.emit(self.currIdx)
            


    def set_state_number(self, idx):
        if 0 <= idx <= self.numStates:
            if idx < self.currIdx:
                # self.scene_handler.reset()
                # self.curr = self.head
                # self.stateChange.emit(0)
                # self.currIdx = 0 
                # for _ in range(self.currIdx, idx, -1):
                self.playBack()
            else:
                for _ in range(self.currIdx, idx):
                    self.playCurr()


