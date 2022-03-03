from manim import *

class AnimationGenerator:
    def __init__(self, mobject_handler):
        self.mobject_handler = mobject_handler

    def reverse(self, animation, state):
        match animation:
            case FadeIn(mobject=mobj):
                mcopy = self.mobject_handler.getCopy(mobj)
                self.mobject_handler.removeCopy(mcopy)
                # mcopy = state.targets[mobj]
                # state.targets[mobj] = mcopy.copy() #gets destroyed so make a new one
                return FadeOut(mcopy)
            case Transform(mobject=mobj, target_mobject=tobj):
                mcopy = self.mobject_handler.getCopy(mobj)
                tcopy = state.targets[mobj].copy()
                self.mobject_handler.setCopy(mobj, tcopy)

                # mcopy_ = state.prev.targets[mobj]
                # tcopy = state.targets[tobj]
                # state.targets[tobj] = tcopy.copy() #gets destroyed
                # self.matchPosition(mcopy_, tcopy)
                return ReplacementTransform(mcopy, tcopy)
            # case ReplacementTransform(mobject=mobj, target_mobject=tobj):
                # mcopy = self.mobject_handler.getCopy(mobj)
                # tcopy = self.mobject_handler.getCopy(tobj)
                # self.mobject_handler.removeCopy(tcopy, mcopy)
                # mcopy_ = self.mobject_handler.getCopy(mobj)
            #     # self.matchPosition(mcopy_, tcopy)
            #     return ReplacementTransform(tcopy, mcopy_)
            case Create(mobject=mobj):
                mcopy = self.mobject_handler.getCopy(mobj)
                self.mobject_handler.removeCopy(mcopy)
                # mcopy = state.targets[mobj]
                # state.targets[mobj] = mcopy.copy() #gets destroyed so make a new one
                return Uncreate(mcopy)
            # case MoveToTarget(mboject=mobj, target_mobject=tobj):
            #     mcopy = self.mobject_handler.getCopy(mobj)
            #     tcopy = self.mobject_handler.getCopy(tobj)
            #     self.mobject_handler.removeCopy(tcopy, mcopy)
            #     mcopy_ = self.mobject_handler.getCopy(mobj)
            #     tcopy.target = mcopy_
            #     return MoveToTarget(tcopy)




    def forward(self, animation, state):
        match animation:
            case Transform(mobject=obj, target_mobject=tobj):
                mcopy = self.mobject_handler.getCopy(obj)
                tcopy = state.next.targets[obj].copy()
                self.mobject_handler.setCopy(obj, tcopy)
                # assert obj in state.prev.targets #should already be introduced
                # mcopy = state.prev.targets[obj]
                # tcopy = state.targets[tobj]
                # state.prev.targets[obj] = mcopy.copy() #gets destroyed so make a new one
                # self.matchPosition(tcopy, mcopy)
                return ReplacementTransform(mcopy, tcopy)
            case FadeIn(mobject=obj):
                mcopy = self.mobject_handler.getCopy(obj) #new
                # state.targets[obj] = mcopy = obj.copy()
                return FadeIn(mcopy)
            case Create(mobject=obj):
                mcopy = self.mobject_handler.getCopy(obj) #new
                # state.targets[obj] = mcopy = obj.copy()
                return Create(mcopy)

            # case MoveToTarget(mboject=obj, target_mobject=tobj):
            #     mcopy = self.mobject_handler.getCopy(obj)
            #     tcopy = self.mobject_handler.getCopy(tobj)
            #     mcopy.target = tcopy
            #     return MoveToTarget(mcopy)
                
                
        
    def matchPosition(self, mobject, target_mobject):
        mobject.match_x(target_mobject)
        mobject.match_y(target_mobject)



            