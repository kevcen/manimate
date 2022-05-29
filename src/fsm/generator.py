from manim import *

from intermediate.ianimation import IApplyFunction, ICreate, IFadeIn, ITransform
import models.mobject_helper as mh;
import copy

def reverse(animation, state):
    if animation.imobject.isDeleted:
        return None

    match animation:
        case IFadeIn(imobject=imobj):
            mcopy = mh.getCopy(imobj)
            mh.removeCopy(mcopy)
            return FadeOut(mcopy)
        case ITransform(imobject=imobj) | IApplyFunction(imobject=imobj):
            mcopy = mh.getCopy(imobj)

            # print('mcopy is ', hex(id(mcopy)))
            tcopy = None
            if imobj in state.prev.targets:
                print('YES TARGET')
                tcopy = state.prev.targets[imobj].copy()
            else:
                print("NO TARGET")
                if imobj.editedAt < state.idx:
                    print("CAPTURE NEW PREV")
                    state.capture_prev(mcopy, bypass=True)
                
                # print('rev target')
                tcopy = state.rev_targets[imobj].copy()

            # print('generate', mcopy.get_center(), tcopy.get_center())
            # mh.setCopy(imobj, tcopy)
            return Transform(mcopy, tcopy)
        case ICreate(imobject=imobj):
            mcopy = mh.getCopy(imobj)
            mh.removeCopy(mcopy)
            return Uncreate(mcopy)

def forward(animation, state):
    if animation.imobject.isDeleted:
        return None

    match animation:
        case ITransform(imobject=imobj):
            mcopy = mh.getCopy(imobj)
            tcopy = state.targets[imobj].copy()
            # mh.setCopy(imobj, tcopy)
            return Transform(mcopy, tcopy)
        case IFadeIn(imobject=imobj):
            mcopy = state.targets[imobj].copy() #target[obj] == obj for introducers
            mh.setCopy(imobj, mcopy)
            return FadeIn(mcopy)
        case ICreate(imobject=imobj):
            mcopy = state.targets[imobj].copy()
            mh.setCopy(imobj, mcopy)
            return Create(mcopy)
        case IApplyFunction(imobject=imobj):
            mcopy = mh.getCopy(imobj)
            # tcopy = state.targets[imobj].copy()
            # mh.setCopy(imobj, tcopy)
            # return Transform(mcopy, tcopy)
            return ApplyFunction(animation.custom_method, mcopy)

def matchPosition(mobject, target_mobject):
    mobject.match_x(target_mobject)
    mobject.match_y(target_mobject)