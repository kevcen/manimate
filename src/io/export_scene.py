from manim import *

class Main(Scene):
    def construct(self):
#PRINT ADDED

#PRINT REMOVED
#PRINT TARGETS
        INode0 = Tree("t", parent=None)
        INode0.move_to([-2.5384615384615388, 1.9076923076923078, 0.0])
        INode1 = Tree("t", parent=INode0)
        INode1.move_to([-4.876923076923077, -0.676923076923077, 0.0])
        IParentEdge0 = ParentEdge(INode1)
        ITriangle0 = Triangle()
        ITriangle0.move_to([0.24615384615384617, 1.8615384615384616, 0.0])
        IStar0 = Star()
        IStar0.move_to([2.9846153846153847, 1.6307692307692307, 0.0])

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
        self.add(INode0)
        self.add(INode1)
        self.add(IParentEdge0)
        self.add(ITriangle0)
        self.add(IStar0)
#PRINT ANIMS
        self.wait(1)
#PRINT ADDED
#PRINT REMOVED
#PRINT TARGETS
        INode1_target = INode1.copy()
        INode1_target.move_to([-0.8769230769230769, -0.5846153846153846, 0.0])
        INode0_target = INode0.copy()
        INode0_target.move_to([-4.523076923076923, 1.6153846153846154, 0.0])

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
#PRINT ANIMS
        self.play(Transform(INode1, INode1_target), Transform(INode0, INode0_target))
#PRINT ADDED
#PRINT REMOVED
#PRINT TARGETS
        INode1_target = INode1.copy()
        INode1_target.move_to([-5.923076923076923, -2.246153846153846, 0.0])

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
#PRINT ANIMS
        self.play(Transform(INode1, INode1_target))
#PRINT ADDED
#PRINT REMOVED
#PRINT TARGETS
        INode1_target = INode1.copy()
        INode1_target.move_to([-1.476923076923077, -2.076923076923077, 0.0])

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
#PRINT ANIMS
        self.play(Transform(INode1, INode1_target))

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
        

class ParentEdge(Line):
    def __init__(self, node):
        self.node = node
        super().__init__(node.parent.get_bottom(), node.get_top(), color=RED)
        self.add_updater(lambda mob: self.updateLine(mob))

    def updateLine(self, line):
        if self.node.parent is None:
            return 

        line.put_start_and_end_on(self.node.parent.get_bottom(),
                    self.node.get_top())

