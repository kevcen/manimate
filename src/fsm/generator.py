from manim import *

from intermediate.ianimation import ICreate, IFadeIn, ITransform

class AnimationGenerator:
    def __init__(self, mobject_handler):
        self.mobject_handler = mobject_handler

    def reverse(self, animation, state):
        match animation:
            case IFadeIn(imobject=imobj):
                mcopy = self.mobject_handler.getCopy(imobj)
                self.mobject_handler.removeCopy(mcopy)
                return FadeOut(mcopy)
            case ITransform(imobject=imobj):
                mcopy = self.mobject_handler.getCopy(imobj)

                tcopy = None
                if imobj in state.prev.targets:
                    tcopy = state.prev.targets[imobj].copy()
                else: 
                    tcopy = state.rev_targets[imobj].copy()

                self.mobject_handler.setCopy(imobj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case ICreate(imobject=imobj):
                mcopy = self.mobject_handler.getCopy(imobj)
                self.mobject_handler.removeCopy(mcopy)
                return Uncreate(mcopy)

    def forward(self, animation, state):
        match animation:
            case ITransform(imobject=imobj):
                mcopy = self.mobject_handler.getCopy(imobj)
                tcopy = state.targets[imobj].copy()
                self.mobject_handler.setCopy(imobj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case IFadeIn(imobject=imobj):
                mcopy = state.targets[imobj].copy() #target[obj] == obj for introducers
                self.mobject_handler.setCopy(imobj, mcopy)
                return FadeIn(mcopy)
            case ICreate(imobject=imobj):
                mcopy = state.targets[imobj].copy()
                self.mobject_handler.setCopy(imobj, mcopy)
                return Create(mcopy)
                
                
        
    def matchPosition(self, mobject, target_mobject):
        mobject.match_x(target_mobject)
        mobject.match_y(target_mobject)



            