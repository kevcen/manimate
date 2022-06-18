from intermediate.ianimation import IApplyFunction, IReplacementTransform, ITransform
from intermediate.imobject import IDependent, IMobject
from intermediate.itree import INode
import controllers.mobject_helper as mh
from pathlib import Path
from manim import VGroup
import os


class Writer:
    """
    Writer class to write the automata controller into a Python script.
    """

    BOILERPLATE = """from manim import *

class Main(Scene):
    def construct(self):
"""

    APPLYFUNCTION = """
    def customfunction(self, mobject, color=None, move_to=None, scale=None):
        if color is not None:
            mobject.set_color(color)
        if move_to is not None:
            mobject.move_to(move_to)
        if scale is not None:
            mobject.scale(scale)
            
        return mobject

"""

    TREECLASS = """
class Tree(VGroup):
    def __init__(self, text="t", parent=None):
        super().__init__()
        self.label = Text(text)
        self.container = Circle(radius=0.6)
        self.add(self.label, self.container)
        self.set_color(RED)
        self.parent = parent

    def change_text_transform(self, text):
        target = Text(text)
        target.match_color(self.label)
        target.move_to(self.label.get_center())

        return Transform(self.label, target)
        
    def set_parent(self, parent):
        self.parent = parent

class ParentEdge(Line):
    def __init__(self, node):
        self.node = node
        super().__init__(
            node.get_bottom() if node.parent is None else node.parent.get_bottom(),
            node.get_top(),
            color=RED,
        )
        self.add_updater(lambda mob: self.update_line(mob))

    def update_line(self, line):
        if self.node.parent is None:
            return 

        line.put_start_and_end_on(self.node.parent.get_bottom(), self.node.get_top())

"""

    def __init__(self, head_state, filename):
        self.head_state = head_state
        self.filename = filename
        self.existing_names = {}
        self.write_apply_function = False
        self.write_tree = False
        self.user_defined_text = {}

    def initialise(self, filename):
        self.existing_names = {}
        self.write_apply_function = False
        self.write_tree = False
        self.filename = filename

    def write(self):
        filepath = Path(self.filename)
        dir_name = self.filename.split('/')[:-1]
        if dir_name:
            dir_name = '/'.join(dir_name)
            os.makedirs(dir_name, exist_ok=True)
            
        filepath.touch(exist_ok=True)
        with open(filepath, "w+", encoding="utf-8") as f:
            f.write(self.BOILERPLATE)
            curr = self.head_state.next
            while curr.next is not None:  # is not the END state
                # add objects
                # self.print_added(f, curr)
                # rem objects
                self.parse_target_equivalences(f, curr)
                self.print_removed(f, curr)

                # attributes
                # self.print_attribute_changes(f, curr)
                self.print_mobject_functions(f, curr)
                self.print_targets(f, curr)

                self.print_modified_added(f, curr)
                # animations
                self.print_animations(f, curr)

                curr = curr.next

            if self.write_apply_function:
                f.write(self.APPLYFUNCTION)

            if self.write_tree:
                f.write(self.TREECLASS)

            for _, text in self.user_defined_text.items():
                f.write(text)
                f.write("\n")

    # debug
    def print_added(self, f, curr):
        # f.write("       #PRINT ADDED\n")
        for imobject in curr.added:
            if imobject.is_deleted:
                continue

            if isinstance(imobject, INode):
                self.write_tree = True
            if imobject.added_state == curr:
                continue  # will be written in targets

            mobj_str = mh.get_name(imobject)
            f.write(f"        {mobj_str} = {imobject.decl_str()}\n")

            if imobject.intro_anim is None:
                f.write(f"        self.add({mobj_str})\n")

        if curr.added:
            f.write("\n")

    def print_removed(self, f, curr):
        # f.write("       #PRINT REMOVED\n")
        for imobject in curr.removed:
            if imobject.is_deleted:
                continue
            f.write(f"        self.remove({mh.get_name(imobject)})\n")

        if curr.removed:
            f.write("\n")

    def print_attribute_changes(self, f, curr):
        pass

    def print_mobject_functions(self, f, curr):
        # f.write("       #PRINT MOBJ FUNCS\n")
        for imobject in curr.called_mobject_functions:
            if imobject.is_deleted:
                continue
            for func, args in curr.called_mobject_functions[imobject].items():
                args_names = [
                    mh.get_name(arg) if isinstance(arg, IMobject) else arg
                    for arg in args
                ]
                mobj_name = mh.get_name(imobject)
                f.write(f"        {mobj_name}.{func}({', '.join(args_names)})\n")

    def print_targets(self, f, curr):
        # f.write("       #PRINT TARGETS\n")

        target_strs = []
        # print vgroup targets first
        for imobject in curr.targets:
            if (
                imobject.is_deleted
                or not isinstance(imobject.mobject, VGroup)
                or isinstance(imobject, IDependent)
            ):
                continue
            target_strs.append(self.print_target_init(f, curr, imobject))

        for imobject in curr.targets:
            if (
                imobject.is_deleted
                or isinstance(imobject.mobject, VGroup)
                or isinstance(imobject, IDependent)
            ):
                continue
            target_strs.append(self.print_target_init(f, curr, imobject))

        for imobject, tobj_str in target_strs:
            self.print_target_manip(f, curr, imobject, tobj_str)

        for imobject in curr.targets:
            if imobject.is_deleted or not isinstance(imobject, IDependent):
                continue

            imobject, tobj_str = self.print_target_init(f, curr, imobject)
            self.print_target_manip(f, curr, imobject, tobj_str)

        if curr.targets:
            f.write("\n")

    def print_target_init(self, f, curr, imobject):
        if isinstance(imobject, INode):
            self.write_tree = True

        tobj_str = (
            mh.get_name(imobject)
            if imobject.added_state == curr or imobject.child_add_state == curr
            else self.get_target_name(imobject, curr)
        )

        target_decl = curr.target_decl_str[imobject]
        f.write(f"        {tobj_str} = {target_decl}\n")

        return imobject, tobj_str

    def print_target_manip(self, f, curr, imobject, tobj_str):
        for func, args in curr.called_target_functions[imobject].items():
            args_names = [
                (
                    self.get_target_name(arg, curr)
                    if arg in curr.targets
                    else mh.get_name(arg)
                )
                if isinstance(arg, IMobject)
                else arg
                for arg in args
            ]
            f.write(f"        {tobj_str}.{func}({', '.join(args_names)})\n")

    def print_modified_added(self, f, curr):
        # f.write("       #PRINT TARGET ADD\n")
        for imobject in curr.targets:
            if imobject.is_deleted:
                continue
            if imobject in curr.added and imobject.intro_anim is None:
                f.write(f"        self.add({mh.get_name(imobject)})\n")

    def print_animations(self, f, curr):
        # f.write("       #PRINT ANIMS\n")
        anim_strs = [
            self.get_anim_str(anim, curr)
            for anim in curr.animations
            if not anim.imobject.is_deleted
        ]
        run_time = f", run_time={str(curr.run_time)}" if curr.run_time != 1.0 else ""
        if anim_strs:
            f.write(f"        self.play({', '.join(anim_strs)})\n")
        else:
            f.write(f"        self.wait({curr.run_time})\n")

    def parse_target_equivalences(self, f, curr):
        for anim in curr.animations:
            if anim.imobject.is_deleted:
                continue

            if isinstance(anim, IReplacementTransform):
                imobject = anim.imobject
                itarget = anim.itarget

                target_str = (
                    mh.get_name(itarget)
                    if itarget.added_state == curr
                    else self.get_target_name(itarget, curr)
                )
                self.existing_names[curr.targets[itarget]] = target_str
                if imobject in curr.targets:
                    self.existing_names[curr.targets[imobject]] = target_str

    def get_anim_str(self, anim, curr):
        res = []

        res.append(anim.__class__.__name__[1:])
        res.append("(")

        imobject = anim.imobject

        match anim:
            case IApplyFunction():
                res.append("self.customfunction")
                res.append(", ")
                res.append(mh.get_name(imobject))
                extra_args = self.get_applyfunction_args_str(anim)
                if extra_args:
                    res.append(", ")
                    res.append(extra_args)
                self.write_apply_function = True
            case ITransform():
                res.append(mh.get_name(imobject))
                res.append(", ")
                res.append(self.use_target_name(imobject, curr))
            case IReplacementTransform():
                res.append(mh.get_name(imobject))
                res.append(", ")
                res.append(self.use_target_name(anim.itarget, curr))
            case _:
                res.append(mh.get_name(imobject))

        res.append(")")

        return "".join(res)

    def get_applyfunction_args_str(self, iapplyfunction):
        res = []
        if iapplyfunction.color is not None:
            res.append(f'"{iapplyfunction.color}"')

        if iapplyfunction.move_to is not None:
            res.append(f"{str(iapplyfunction.move_to.tolist())}")

        if iapplyfunction.scale is not None:
            res.append(f"{str(iapplyfunction.scale)}")

        return ", ".join(res)

    def get_target_name(self, imobject, curr):
        target = curr.targets[imobject]
        if target not in self.existing_names:
            mobj_name = mh.get_name(imobject)
            self.existing_names[target] = f"{mobj_name}_target"

        return self.existing_names[target]

    def use_target_name(self, imobject, curr):
        target = curr.targets[imobject]
        tname = self.existing_names[target]
        del self.existing_names[target]
        return tname

    def get_latest_name(self, imobject, curr):
        if imobject in curr.targets:
            target = curr.targets[imobject]
            if imobject in self.existing_names[target]:
                return self.existing_names[target]
        return mh.get_name(imobject)
