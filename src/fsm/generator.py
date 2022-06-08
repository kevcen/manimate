from manim import *

from intermediate.ianimation import ICreate, IFadeIn, IReplacementTransform, ITransform
import models.mobject_helper as mh


def reverse(animation, state):
    """
    Gives the reverse animation given an IAnimation and the current state.
    """

    if animation.imobject.is_deleted:
        return None

    print("REVERSE", animation, animation.imobject.mobject)
    match animation:
        case IFadeIn(imobject=imobj):
            mcopy = mh.get_copy(imobj)
            mh.remove_copy(mcopy)
            return FadeOut(mcopy)
        case ITransform(imobject=imobj):
            mcopy = mh.get_copy(imobj)

            irtobj = None
            if imobj.key_imobject in state.prev.targets:
                irtobj = state.prev.get_target(imobj)
            else:
                edit_idx = imobj.key_imobject.edited_at
                if edit_idx is not None and edit_idx < state.idx:
                    state.capture_prev(imobj, force=True)

                irtobj = state.rev_targets[imobj.key_imobject]

            # mh.set_original(mcopy, irtobj)
            rtcopy = irtobj.mobject.copy()# TODO: do we use generatecopy?
            return Transform(mcopy, rtcopy)
        case IReplacementTransform(imobject=imobj, itarget=itobj):
            tcopy = mh.get_copy(imobj)

            mcopy = mh.get_reverse_copy(imobj, state) #TODO: use gencopy?
            print("REVERSED TRANSFORM TO", mcopy)
            # mh.remove_copy(tcopy)
            mh.set_copy(imobj, mcopy)
            return ReplacementTransform(tcopy, mcopy)
        case ICreate(imobject=imobj):
            mcopy = mh.get_copy(imobj)
            mh.remove_copy(mcopy)
            return Uncreate(mcopy)


def forward(animation, state):
    """
    Returns the forward animation given an IAnimation and the current state
    """
    if animation.imobject.is_deleted:
        return None

    match animation:
        case ITransform(imobject=imobj):
            mcopy = mh.get_copy(imobj)
            tcopy = state.get_target(imobj).mobject.copy()
            # mh.set_copy(imobj, tcopy)
            return Transform(mcopy, tcopy)
        case IReplacementTransform(imobject=imobj, itarget=itobj):
            print("PLAY FORWARD REPLACEMENTTRANSFORM")
            mcopy = mh.get_copy(imobj)
            tcopy = state.get_target(imobj).mobject.copy()
            mh.remove_copy(mcopy)
            mh.set_copy(imobj, tcopy)
            return ReplacementTransform(mcopy, tcopy)
        case IFadeIn(imobject=imobj):
            mcopy = state.get_target(imobj).mobject.copy()  # target[obj] == obj for introducers
            mh.set_copy(imobj, mcopy)
            return FadeIn(mcopy)
        case ICreate(imobject=imobj):
            mcopy = state.get_target(imobj).mobject.copy()
            mh.set_copy(imobj, mcopy)
            return Create(mcopy)
        # case IApplyFunction(imobject=imobj):
        #     mcopy = mh.get_copy(imobj)
        #     # tcopy = state.get_target(imobj).copy()
        #     # mh.set_copy(imobj, tcopy)
        #     # return Transform(mcopy, tcopy)
        #     return ApplyFunction(animation.custom_method, mcopy)

