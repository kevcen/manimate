import collections
from manim import *

class Writer:
    BOILERPLATE = "from manim import *\n\nclass Main(Scene):\n  def construct(self):\n" 
    def __init__(self, head_state, filename="scene/output_scene.py"):
        self.head_state = head_state
        self.filename = filename
        self.class_counters = collections.defaultdict(int) #mobject class -> counter
        self.existing_names = {}

    def write(self):
        with open(self.filename, "w") as f:
            f.write(self.BOILERPLATE)
            curr = self.head_state 
            while curr.next is not None: # is not the END state
                # self.print_targets(f, curr, init=True)
                # self.print_added(f, curr)
                self.print_targets(f, curr.next)
                
                self.print_animations(f, curr)

                curr = curr.next

    def print_added(self, f, curr):
        for mobject in curr.added:
            mobj_str = self.get_mobject_str(mobject)
            f.write(f"    {mobj_str} = {mobject.__class__.__name__}()\n")
            
    def print_targets(self, f, curr, init=False):
        for mobject, tobject in curr.targets.items():
            tobj_str = self.get_mobject_str(tobject)
            f.write(f"    {tobj_str} = {tobject.__class__.__name__}()\n")

            for attr, value in curr.changedTargetAttributes[mobject].items():
                f.write(f"    {tobj_str}.{attr}({value})\n")

            f.write('\n')
            
    def print_animations(self, f, curr):
        anim_strs = [self.get_anim_str(anim) for anim in curr.animations]
        if anim_strs:
            f.write(f"    self.play({', '.join(anim_strs)})\n")
        else:
            f.write("    self.wait(1)\n")


    def get_anim_str(self, anim):
        res = []

        res.append(anim.__class__.__name__)
        res.append('(')

        res.append(self.get_mobject_str(anim.mobject))

        match anim:
            case Transform(mobject=mobj, target_mobject=tobj):
                res.append(', ')
                res.append(self.get_mobject_str(anim.target_mobject))
            case default:
                pass

        res.append(')')

        return ''.join(res)

    def get_mobject_str(self, mobject):
        if mobject not in self.existing_names:
            self.existing_names[mobject] = mobject.__class__.__name__ + str(self.class_counters[mobject.__class__])
            self.class_counters[mobject.__class__] += 1

        return self.existing_names[mobject]

                
                


    
        