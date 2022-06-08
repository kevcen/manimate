from collections import defaultdict
from contextvars import copy_context
from bidict import bidict
from manim import VGroup

"""
Module which handles the linking of intermediate mobjects, IMobjects,
and actual manim mobjects
"""

copies = bidict()
names = bidict()
classCtr = defaultdict(int)
groups = set()


def get_groups():
    return groups


def get_copy(imobject):
    imobject = imobject.key_imobject
    # imobject = state.get_target(imobject)
    if imobject not in copies:
        print("GET COPY")
        set_copy(imobject, generate_new_copy(imobject))

    return copies[imobject]


def generate_new_copy(imobject, mcopy=None, use_current=False):
    # curr_imobject = None
    # if imobject not in state.targets and is_reverse:
    #     curr_imobject = state.next.rev_targets[imobject]
    # else:
    #     curr_imobject = state.get_target(imobject)
    if isinstance(imobject.mobject, VGroup):
        print("VGROUP COPY")
        vgroup_children = [generate_new_copy(child, use_current=False) for child in imobject.vgroup_children]
        vgroup = VGroup(*vgroup_children)
        vgroup.set_color(imobject.mobject.get_color())
        print(vgroup)
        return vgroup

    # normal copy
    if mcopy is None:
        print("GENERATE MCOPY")
        mcopy = get_copy(imobject) if use_current else imobject.mobject.copy()
        print(mcopy, mcopy.get_center().tolist())
    return mcopy

def get_reverse_copy(imobject, state):
    if imobject.key_imobject in state.prev.targets:
        irtobj = state.prev.get_target(imobject)
        print("TARGETS PREV of ", imobject, irtobj)
    else:
        edit_idx = imobject.key_imobject.edited_at
        if imobject.key_imobject not in state.rev_targets or (edit_idx is not None and edit_idx < state.idx):
            state.capture_prev(imobject, force=True)

        # print('rev target')
        irtobj = state.rev_targets[imobject.key_imobject]
        print("PREV of ", imobject, irtobj)

    if isinstance(irtobj.mobject, VGroup):
        print("VGROUP REVERSE COPY")
        vgroup_children = [get_reverse_copy(child, state) for child in irtobj.vgroup_children]
        vgroup = VGroup(*vgroup_children)
        vgroup.set_color(irtobj.mobject.get_color())
        print(vgroup)
        return vgroup

    return irtobj.mobject.copy()

def remove_copy(*mcopies):
    for mcopy in mcopies:
        original = copies.inverse[mcopy]
        del copies[original]


def set_copy(imobject, mcopy):
    copies[imobject] = mcopy

def set_original(mcopy, imobject):
    if mcopy in copies.inverse:
        remove_copy(mcopy)

    set_copy(imobject, mcopy)
    # copies.inverse[mcopy] = imobject


def get_original(mcopy):
    return copies.inverse[mcopy] if mcopy in copies.inverse else None


def get_name(imobject):
    imobject = imobject.key_imobject
    if imobject not in names:
        cnt = classCtr[imobject.__class__]
        set_name(imobject, imobject.__class__.__name__ + str(cnt))
        classCtr[imobject.__class__] += 1

    return names[imobject]


def set_name(imobject, name):
    imobject = imobject.key_imobject
    if name in names.inverse:
        return False  # already in use

    names[imobject] = name
    return True


def get_imobject_by_name(name):
    if name not in names.inverse:
        return None

    return names.inverse[name]


def get_imobjects_by_class(cls):
    for imobj in copies:
        if isinstance(imobj, cls):
            yield imobj
