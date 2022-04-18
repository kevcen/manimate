from manim import *

class AnimationGenerator:
    def __init__(self, mobject_handler):
        self.mobject_handler = mobject_handler

    def reverse(self, animation, state):
        match animation:
            case FadeIn(mobject=mobj):
                mcopy = self.mobject_handler.getCopy(mobj)
                self.mobject_handler.removeCopy(mcopy)
                return FadeOut(mcopy)
            case Transform(mobject=mobj, target_mobject=tobj):
                mcopy = self.mobject_handler.getCopy(mobj)
                tcopy = state.targets[mobj].copy()
                self.mobject_handler.setCopy(mobj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case Create(mobject=mobj):
                mcopy = self.mobject_handler.getCopy(mobj)
                self.mobject_handler.removeCopy(mcopy)
                return Uncreate(mcopy)

    def forward(self, animation, state):
        match animation:
            case Transform(mobject=obj, target_mobject=tobj):
                mcopy = self.mobject_handler.getCopy(obj)
                tcopy = state.next.targets[obj].copy()
                self.mobject_handler.setCopy(obj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case FadeIn(mobject=obj):
                mcopy = state.next.targets[obj].copy() #target[obj] == obj for introducers
                self.mobject_handler.setCopy(obj, mcopy)
                return FadeIn(mcopy)
            case Create(mobject=obj):
                mcopy = state.next.targets[obj].copy()
                self.mobject_handler.setCopy(obj, mcopy)
                return Create(mcopy)
                
                
        
    def matchPosition(self, mobject, target_mobject):
        mobject.match_x(target_mobject)
        mobject.match_y(target_mobject)



            