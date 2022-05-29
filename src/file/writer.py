import collections
from manim import *

from intermediate.ianimation import IApplyFunction, ICreate, IFadeIn, ITransform
import  models.mobject_helper as mh

class Writer:
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

    def __init__(self, head_state, filename="scene/output_scene.py"):
        self.head_state = head_state
        self.filename = filename
        self.existing_names = {}
        self.writeApplyFunction = False
        self.writeTree = False

    def write(self):
        with open(self.filename, "w") as f:
            f.write(self.BOILERPLATE)
            curr = self.head_state.next 
            while curr.next is not None: # is not the END state
                #add objects
                self.print_added(f, curr)
                #rem objects
                self.print_removed(f, curr)

                #attributes
                # self.print_attribute_changes(f, curr)

                #animations
                self.print_targets(f, curr)
                self.print_animations(f, curr)

                curr = curr.next

            # if self.writeTree:
            #     self.print_tree_class(f)
            
            if self.writeApplyFunction:
                f.write(self.APPLYFUNCTION)

    #debug
    def print_added(self, f, curr):
        for imobject in curr.added:
            if imobject.addedState == curr:
                continue #will be written in targets

            mobj_str = mh.getName(imobject)
            f.write(f"        {mobj_str} = {imobject.declStr()}\n")
            
            if imobject.introAnim is None:
                f.write(f"        self.add({mobj_str})\n")

        if curr.added:
            f.write('\n')

    def print_removed(self, f, curr):
        for imobject in curr.removed:
            f.write(f"        self.remove({mh.getName(imobject)})\n")
        
        if curr.removed:
            f.write('\n')

    def print_attribute_changes(self, f, curr):
        pass
            
    def print_targets(self, f, curr):
        for imobject in curr.targets:
            tobj_str = mh.getName(imobject) if imobject.addedState == curr else self.get_target_name(imobject, curr)

            target_decl = curr.targetDeclStr[imobject]
            f.write(f"        {tobj_str} = {target_decl}\n")

            for func, args in curr.calledTargetFunctions[imobject].items():
                f.write(f"        {tobj_str}.{func}({', '.join(args)})\n")

            
            if curr == imobject.addedState and imobject.introAnim is None:
                f.write(f"        self.add({tobj_str})\n")

        if curr.targets:
            f.write('\n')

        
            
    def print_animations(self, f, curr):
        anim_strs = [self.get_anim_str(anim, curr) for anim in curr.animations]
        if anim_strs:
            f.write(f"        self.play({', '.join(anim_strs)})\n")
        else:
            f.write("        self.wait(1)\n")


    def get_anim_str(self, anim, curr):
        res = []

        res.append(anim.__class__.__name__[1:])
        res.append('(')

        imobject = anim.imobject
        match anim:
            case IApplyFunction():
                res.append('self.customfunction')
                res.append(', ')
                res.append(mh.getName(imobject))
                extra_args = self.get_applyfunction_args_str(anim)
                if extra_args:
                    res.append(', ')
                    res.append(extra_args)
                self.writeApplyFunction = True
            case ITransform():
                res.append(mh.getName(imobject))
                res.append(', ')
                res.append(self.get_target_name(imobject, curr))
            case _:
                res.append(mh.getName(imobject))

        res.append(')')

        return ''.join(res)

    def get_applyfunction_args_str(self, iapplyfunction):
        res = []
        if iapplyfunction.color is not None:
            res.append(f"\"{iapplyfunction.color}\"")
        
        if iapplyfunction.move_to is not None:
            res.append(f"{str(iapplyfunction.move_to.tolist())}")
        
        if iapplyfunction.scale is not None:
            res.append(f"{str(iapplyfunction.scale)}")

        print("APPLYFUNCTION ARGS", res)
        return ', '.join(res)


    def get_target_name(self, imobject, curr):
        target = curr.targets[imobject]
        if target not in self.existing_names:
            mobj_name = mh.getName(imobject)
            self.existing_names[target] = f"{mobj_name}_target"

        return self.existing_names[target]



                
                


    
        