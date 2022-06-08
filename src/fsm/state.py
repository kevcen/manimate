from collections import defaultdict, OrderedDict

from intermediate.ianimation import IReplacementTransform, ITransform
import fsm.generator as generator
import models.mobject_helper as mh
from manim import VGroup

class State:
    """
    A single state of the automata-based animation model.
    """
    def __init__(self, idx, animations=None):
        self.next = None  # next state
        self.prev = None  # previous state
        self.animations = animations if animations else []  # list of animations to play
        self.targets = OrderedDict()  # what the mobjects look like at this state at the end
        self.rev_targets = {}
        self.transforms = {}
        # self.applyfunctions = {}
        ## TODO: replace transforms by using prepare_anim on called_target_functions
        # imobject -> function -> set(args)
        self.called_mobject_functions = defaultdict(lambda: defaultdict(lambda: set()))
        self.called_target_functions = defaultdict(lambda: defaultdict(lambda: set()))
        self.target_decl_str = {}
        self.rev_attributes = defaultdict(lambda: {})
        self.changed_mobject_attributes = defaultdict(lambda: {})
        self.added = []
        self.removed = []
        self.idx = idx
        self.run_time = 1.0
        self.loop = None  # in form of (state, times)
        self.loop_cnt = None

    def add_transform(self, imobject):
        """
        PRE: called only after state has a target for the transform
        """
        imobject = imobject.key_imobject
        assert imobject in self.targets

        if imobject not in self.transforms:
            self.transforms[imobject] = ITransform(imobject)
            self.animations.append(self.transforms[imobject])

        return self.transforms[imobject]

    def add_replacement_transform(self, imobject, itarget):
        if imobject in self.transforms and self.transforms[imobject] in self.animations:
            self.animations.remove(self.transforms[imobject])
        self.transforms[imobject] = IReplacementTransform(imobject, itarget)
        self.animations.append(self.transforms[imobject])

    def get_transform(self, imobject):
        return self.transforms[imobject] if imobject in self.transforms else None

    # def add_apply_function(self, imobject):
    #     if imobject not in self.applyfunctions:
    #         self.applyfunctions[imobject] = IApplyFunction(imobject)
    #         self.animations.append(self.applyfunctions[imobject])

    #     return self.applyfunctions[imobject]

    # def get_apply_function(self, imobject):
    #     return (
    #         self.applyfunctions[imobject] if imobject in self.applyfunctions else None
    #     )

    # Capturing states for reverse
    def capture_prev(self, imobject, force=False, capture_children=False):
        # print('try capture', hex(id(self)))
        # capture previous frame for reverse if editable
        imobjs = [imobject.key_imobject]
        if capture_children and isinstance(imobject.mobject, VGroup):
            for child in imobject.vgroup_children:
                child = child.key_imobject
                imobjs.append(child)

        for imobj in imobjs:
            if not force and imobj in self.rev_targets:  # if not already captured
                continue
            
            # print("ATTEMPT CAPTURE", imobj)
            target = self.prev.find_prev_target(imobj)
            if target is None:
                continue  # we are in head state

            self.rev_targets[imobj] = target
            edit_idx = imobj.edited_at
            if edit_idx is not None and edit_idx < self.idx:
                imobj.edited_at = None  # mark as handled

        if capture_children and isinstance(imobject.mobject, VGroup):
            print("CHILDREN CAPTURED", len(imobjs) -1)
            self.rev_targets[imobject.key_imobject].mobject.add(*[self.rev_targets[child].mobject.copy() for child in imobjs[1:]])

    def find_prev_target(self, imobject):
        if imobject in self.targets:
            print("RETRIEVE STATE ", self.idx, imobject)
            return self.get_target(imobject) #TODO: do something with vgroup - prob not, children have targets
        
        if self.prev is None:
            return None

        return self.prev.find_prev_target(imobject)
    
    def get_target(self, imobject):
        imobject = imobject.key_imobject
        return self.targets[imobject]

    def change_target_mobject(self, imobject, mobject):
        key_imobject = imobject.key_imobject
        if key_imobject not in self.targets:
            # print(key_imobject)
            self.targets[key_imobject] = imobject.copy()
        self.get_target(key_imobject).mobject = mobject
        print(len(self.targets), "TARGTE LEN")

    # Scene related functions
    def play_one(self, anim, scene):
        anim.run_time = 0
        scene.play(anim)

    def play_copy(self, anim, scene):
        forward_anim = generator.forward(anim, self)
        forward_anim.run_time = 0
        scene.play(forward_anim)

    def add_mobjects(self, mobjects, scene):
        for imobject in mobjects:
            mcopy = mh.get_copy(imobject)
            if isinstance(imobject.mobject, VGroup):
                mcopy = VGroup()
                for child in imobject.vgroup_children:
                    ccopy = mh.generate_new_copy(child)
                    mh.set_copy(child.key_imobject, ccopy)
                    mcopy.add(ccopy)
            scene.add(mcopy)

    def remove_mobjects(self, mobjects, scene):
        for imobject in mobjects:
            mcopy = mh.get_copy(imobject)
            print("REMOVE", mcopy)
            scene.remove(mcopy)
            if isinstance(imobject.mobject, VGroup):
                for child in imobject.vgroup_children:
                    print("READD GROUP CHILD ", child.mobject)
                    ccopy = mh.generate_new_copy(child)
                    mh.set_copy(child.key_imobject, ccopy)
                    scene.add(ccopy)

    def forward_attributes(self):
        for imobject in self.changed_mobject_attributes:
            for attr_name, value in self.changed_mobject_attributes[imobject].items():
                setattr(imobject, attr_name, value)

    def reverse_attributes(self):
        for imobject in self.changed_mobject_attributes:
            for attr_name in self.changed_mobject_attributes[imobject]:
                value = None
                if attr_name in self.prev.changed_mobject_attributes[imobject]:
                    value = self.prev.changed_mobject_attributes[imobject][attr_name]
                else:
                    value = self.rev_attributes[imobject][attr_name]
                # print(imobject, attr_name, value)
                setattr(imobject, attr_name, value)

    def play(self, scene, fast=False):
        self.add_mobjects(self.added, scene)
        self.remove_mobjects(self.removed, scene)
        self.forward_attributes()
        forward_anim = list(
            filter(None, map(lambda a: generator.forward(a, self), self.animations))
        )

        for animation in forward_anim:
            animation.run_time = self.run_time if not fast else 0

        if len(forward_anim) > 0:
            scene.play(*forward_anim)
        elif not fast:
            scene.wait(1)

    def play_rev(self, scene):
        # print(f"rem {len(state.added)}, anim {len(state.animations)}")
        reversed_anim = list(
            filter(None, map(lambda a: generator.reverse(a, self), self.animations))
        )

        for animation in reversed_anim:
            # print('rev', animation, animation.mobject)
            animation.run_time = 0

        if len(reversed_anim) > 0:
            scene.play(*reversed_anim)

        self.add_mobjects(self.removed, scene)
        self.remove_mobjects(self.added, scene)
        self.reverse_attributes()

    ## debugging
    def replay(self, scene):
        reversed_anim = [generator.reverse(instr, self) for instr in self.animations]

        for animation in reversed_anim:
            animation.run_time = 0

        if reversed_anim:
            scene.play(*reversed_anim)

        forward_anim = [generator.forward(anim, self) for anim in self.animations]
        for animation in forward_anim:
            animation.run_time = 0

        if forward_anim:
            scene.play(*forward_anim)
