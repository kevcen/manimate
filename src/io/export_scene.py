from manim import *

class Main(Scene):
    def construct(self):
#PRINT ADDED

#PRINT REMOVED
#PRINT TARGETS
        IStar0 = Star()
        self.add(IStar0)
        IStar1 = Star()
        self.add(IStar1)

#PRINT MOBJ FUNCS
        IStar0.move_to([-4.753846153846154, 2.769230769230769, 0.0])
        IStar1.move_to([-5.0769230769230775, -2.0307692307692307, 0.0])
#PRINT ANIMS
        self.wait(1)
#PRINT ADDED

#PRINT REMOVED
#PRINT TARGETS
        IStar2 = Star()
        self.add(IStar2)
        IGroup0 = VGroup()
        self.add(IGroup0)

#PRINT MOBJ FUNCS
        IStar2.move_to([-1.830769230769231, 2.9384615384615387, 0.0])
        IGroup0.add(IStar0)
        IGroup0.add(IStar1)
        IGroup0.add(IStar2)
#PRINT ANIMS
        self.wait(1)
#PRINT ADDED
#PRINT REMOVED
#PRINT TARGETS
        IGroup0_target = IGroup0.copy()

#PRINT MOBJ FUNCS
        IGroup0_target.move_to([0.3076923076923077, 0.07692307692307693, 0.0])
#PRINT ANIMS
        self.play(Transform(IGroup0, IGroup0_target))
