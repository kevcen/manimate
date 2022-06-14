from manim import *

from intermediate.ianimation import (
    IApplyFunction,
    ICreate,
    IFadeIn,
    IReplacementTransform,
    ITransform,
)
import controllers.mobject_helper as mh


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
                print("use target")
                tcopy = state.prev.targets[imobj].copy()
            else:
                print("use rev target")
                if imobj not in state.rev_targets or (
                    imobj.edited_at is not None and imobj.edited_at < state.idx
                ):
                    state.capture_prev(mcopy, bypass=True)

                # print('rev target')
                tcopy = state.rev_targets[imobj].copy()

            # print('generate', mcopy.get_center(), tcopy.get_center())
            # mh.set_copy(imobj, tcopy)
            return Transform(mcopy, tcopy)
        case IReplacementTransform(imobject=imobj, itarget=itobj):
            mcopy = mh.get_copy(itobj)

            tcopy = None
            if imobj in state.prev.targets:
                print("use targets")
                tcopy = state.prev.targets[imobj].copy()
            else:
                if imobj not in state.rev_targets or (
                    imobj.edited_at is not None and imobj.edited_at < state.idx
                ):
                    state.capture_prev(mcopy, bypass=True)

                print("rev target")
                tcopy = state.rev_targets[imobj].copy()

            mh.remove_copy(mcopy)
            if not itobj.user_defined and isinstance(itobj.mobject, VGroup):
                for child in itobj.vgroup_children:
                    mh.remove_copy(mh.get_copy(child))
            mh.set_copy(imobj, tcopy)
            return ReplacementTransform(mcopy, tcopy)
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
            # mh.set_copy(imobj, tcopy)
            return Transform(mcopy, tcopy)
        case IReplacementTransform(imobject=imobj, itarget=itobj):
            mcopy = mh.get_copy(imobj)
            tcopy = mh.generate_new_copy(
                itobj, child_state=state, default=state.targets[itobj].copy()
            )
            # mh.set_copy(imobj, tcopy)
            mh.remove_copy(mcopy)
            mh.set_copy(itobj, tcopy)
            return ReplacementTransform(mcopy, tcopy)
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
            # mh.set_copy(imobj, tcopy)
            # return Transform(mcopy, tcopy)
            return ApplyFunction(animation.custom_method, mcopy)
