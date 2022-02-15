import sys
from PySide6.QtCore import (Signal, QObject)
from fsm.state import State
from manim import *



class StateHandler(QObject):
    stateChange = Signal(int)

    def __init__(self, scene_handler):
        super().__init__()

        self.numStates = 2
        self.scene_handler = scene_handler
        c1 = Circle()
        s1 = Square()
        self.head = State([FadeIn(c1), Create(s1)])
        self.head.next = State([ReplacementTransform(c1, Square())])

        self.is_running = False
        
        self.curr = self.head
        self.currIdx = 0
         
    def playCurr(self):
        self.currIdx += 1
        self.scene_handler.playFast(self.curr)
        self.curr = self.curr.next

    def run(self):
        # self.is_running = True
        while self.curr:
            self.playCurr()


    def set_state_number(self, idx):
        if 0 <= idx <= self.numStates:
            if idx < self.currIdx:
                self.scene_handler.reset()
                self.curr = self.head
                self.stateChange.emit(0)
                self.currIdx = 0 
            else:
                for _ in range(self.currIdx, idx):
                    self.playCurr()


