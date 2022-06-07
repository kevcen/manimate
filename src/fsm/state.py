from bidict import bidict
from collections import defaultdict

from intermediate.ianimation import IApplyFunction, IReplacementTransform, ITransform
import fsm.generator as generator
import models.mobject_helper as mh

class State:
    """
    A single state of the automata-based animation model.
    """
    def __init__(self, idx, animations=None):
        self.next = None  # next state
        self.prev = None  # previous state
        self.animations = animations if animations else []  # list of animations to play
        self.targets = bidict()  # what the mobjects look like at this state at the end
        self.rev_targets = bidict()
        self.transforms = {}
        self.applyfunctions = {}
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
        self.loopCnt = None

    def add_transform(self, imobject):
        """
        PRE: called only after state has a target for the transform
        """
        assert imobject in self.targets

        if imobject not in self.transforms:
            self.transforms[imobject] = ITransform(imobject)
            self.animations.append(self.transforms[imobject])

        return self.transforms[imobject]

    def add_replacement_transform(self, imobject):
        if imobject in self.transforms and self.transforms[imobject] in self.animations:
            self.animations.remove(self.transforms[imobject])
        self.transforms[imobject] = IReplacementTransform(imobject)
        self.animations.append(self.transforms[imobject])

    def get_transform(self, imobject):
        return self.transforms[imobject] if imobject in self.transforms else None

    def add_apply_function(self, imobject):
        if imobject not in self.applyfunctions:
            self.applyfunctions[imobject] = IApplyFunction(imobject)
            self.animations.append(self.applyfunctions[imobject])

        return self.applyfunctions[imobject]

    def get_apply_function(self, imobject):
        return (
            self.applyfunctions[imobject] if imobject in self.applyfunctions else None
        )

    # Capturing states for reverse
    def capture_prev(self, mcopy, bypass=False):
        # print('try capture', hex(id(self)))
        # capture previous frame for reverse if editable
        imobject = mh.get_original(mcopy)
        if bypass or imobject not in self.rev_targets:  # if not already captured
            target = self.find_prev_target(self.prev, imobject)
            if target is None:
                return  # we are in head state

            self.rev_targets[imobject] = target
            if imobject.edited_at is not None and imobject.edited_at < self.idx:
                imobject.edited_at = None  # mark as handled

    def find_prev_target(self, state, imobject):
        if state is None:
            return None

        if imobject in state.targets:
            return state.targets[imobject].copy()
        return self.find_prev_target(state.prev, imobject)

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
            scene.add(mcopy)

    def remove_mobjects(self, mobjects, scene):
        for imobject in mobjects:
            mcopy = mh.get_copy(imobject)
            scene.remove(mcopy)

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
