from manim import *

from intermediate.ianimation import ICreate, IFadeIn, ITransform
import models.mobject_helper as mh;
import copy

class AnimationGenerator:

    def reverse(self, animation, state):
        if animation.imobject.isDeleted:
            return None

        match animation:
            case IFadeIn(imobject=imobj):
                mcopy = mh.getCopy(imobj)
                mh.removeCopy(mcopy)
                return FadeOut(mcopy)
            case ITransform(imobject=imobj):
                mcopy = mh.getCopy(imobj)

                # print('mcopy is ', hex(id(mcopy)))
                tcopy = None
                if imobj in state.prev.targets:
                    # print('have target')
                    tcopy = state.prev.targets[imobj].copy()
                else:
                    if imobj.editedAt < state.idx:
                        state.capture_prev(mcopy, bypass=True)
                    
                    # print('rev target')
                    tcopy = state.rev_targets[imobj].copy()

                # print('generate', mcopy.get_center(), tcopy.get_center())
                mh.setCopy(imobj, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            case ICreate(imobject=imobj):
                mcopy = mh.getCopy(imobj)
                mh.removeCopy(mcopy)
                return Uncreate(mcopy)

    def forward(self, animation, state):
        if animation.imobject.isDeleted:
            return None

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



            