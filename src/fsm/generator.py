from manim import *

from intermediate.ianimation import ICreate, IFadeIn, ITransform
import models.mobject_helper as mh;

class AnimationGenerator:

    def reverse(self, animation, state):
        match animation:
            case IFadeIn(imobject=imobj):
                mcopy = mh.getCopy(imobj)
                mh.removeCopy(mcopy)
                return FadeOut(mcopy)
            case ITransform(imobject=imobj):
                mcopy = mh.getCopy(imobj)

                tcopy = None
                if imobj in state.prev.targets:
                    tcopy = state.prev.targets[imobj].copy()
                else: 
                    tcopy = state.rev_targets[imobj].copy()

                mh.setCopy(imobj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case ICreate(imobject=imobj):
                mcopy = mh.getCopy(imobj)
                mh.removeCopy(mcopy)
                return Uncreate(mcopy)

    def forward(self, animation, state):
        match animation:
            case ITransform(imobject=imobj):
                mcopy = mh.getCopy(imobj)
                tcopy = state.targets[imobj].copy()
                mh.setCopy(imobj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case IFadeIn(imobject=imobj):
                mcopy = state.targets[imobj].copy() #target[obj] == obj for introducers
                mh.setCopy(imobj, mcopy)
                return FadeIn(mcopy)
            case ICreate(imobject=imobj):
                mcopy = state.targets[imobj].copy()
                mh.setCopy(imobj, mcopy)
                return Create(mcopy)
                
                
        
    def matchPosition(self, mobject, target_mobject):
        mobject.match_x(target_mobject)
        mobject.match_y(target_mobject)



            