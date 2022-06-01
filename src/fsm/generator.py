from manim import *

from intermediate.ianimation import IApplyFunction, ICreate, IFadeIn, ITransform
import models.mobject_helper as mh


def reverse(animation, state):
    """
    Gives the reverse animation given an IAnimation and the current state.
    """

    if animation.imobject.is_deleted:
        return None

    match animation:
        case IFadeIn(imobject=imobj):
            mcopy = mh.get_copy(imobj)
            mh.remove_copy(mcopy)
            return FadeOut(mcopy)
        case ITransform(imobject=imobj) | IApplyFunction(imobject=imobj):
            mcopy = mh.get_copy(imobj)

            tcopy = None
            if imobj in state.prev.targets:
                tcopy = state.prev.targets[imobj].copy()
            else:
                if imobj.edited_at < state.idx:
                    state.capture_prev(mcopy, bypass=True)

                # print('rev target')
                tcopy = state.rev_targets[imobj].copy()

            # print('generate', mcopy.get_center(), tcopy.get_center())
            # mh.setCopy(imobj, tcopy)
            return Transform(mcopy, tcopy)
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
            tcopy = state.targets[imobj].copy()
            # mh.setCopy(imobj, tcopy)
            return Transform(mcopy, tcopy)
        case IFadeIn(imobject=imobj):
            mcopy = state.targets[imobj].copy()  # target[obj] == obj for introducers
            mh.set_copy(imobj, mcopy)
            return FadeIn(mcopy)
        case ICreate(imobject=imobj):
            mcopy = state.targets[imobj].copy()
            mh.set_copy(imobj, mcopy)
            return Create(mcopy)
        case IApplyFunction(imobject=imobj):
            mcopy = mh.get_copy(imobj)
            # tcopy = state.targets[imobj].copy()
            # mh.setCopy(imobj, tcopy)
            # return Transform(mcopy, tcopy)
            return ApplyFunction(animation.custom_method, mcopy)

