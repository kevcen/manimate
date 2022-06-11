from collections import defaultdict
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
    if imobject not in copies:
        print('new copy generate')
        set_copy(imobject, generate_new_copy(imobject))

    return copies[imobject]


def generate_new_copy(imobject, default=None):
    if isinstance(imobject.mobject, VGroup):
        vgroup_children = [get_copy(child) for child in imobject.vgroup_children]
        vgroup = VGroup(*vgroup_children)
        # if imobject.color_changed:
        #     print("COLOR CHANGED VGROUP")
        print("linking children")
        vgroup.set_color(imobject.mobject.get_color())
        if default is not None:
            vgroup.move_to(default)
        return vgroup

    mcopy = imobject.mobject.copy() if default is None else default
    return mcopy


def remove_copy(*mcopies):
    for mcopy in mcopies:
        original = copies.inverse[mcopy]
        del copies[original]


def set_copy(mobject, mcopy):
    copies[mobject] = mcopy


def get_original(mcopy):
    return copies.inverse[mcopy] if mcopy in copies.inverse else None


def get_name(imobject):
    if imobject not in names:
        cnt = classCtr[imobject.__class__]
        set_name(imobject, imobject.__class__.__name__ + str(cnt))
        classCtr[imobject.__class__] += 1

    return names[imobject]


def set_name(imobject, name):
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
