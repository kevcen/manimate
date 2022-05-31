from manim import *

class Main(Scene):
    def construct(self):
#PRINT ADDED

#PRINT REMOVED
#PRINT TARGETS
        INode0 = Tree("t", parent=None)
        INode0.move_to([-4.276923076923077, 2.3692307692307693, 0.0])
        INode1 = Tree("t", parent=INode0)
        INode1.move_to([-4.276923076923077, 0.36923076923076925, 0])
        IParentEdge0 = ParentEdge(INode1)
        INode2 = Tree("t", parent=INode1)
        INode2.move_to([-4.276923076923077, -1.6307692307692307, 0])
        IParentEdge1 = ParentEdge(INode2)

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
        self.add(INode0)
        self.add(INode1)
        self.add(IParentEdge0)
        self.add(INode2)
        self.add(IParentEdge1)
#PRINT ANIMS
        self.wait(1)
#PRINT ADDED
#PRINT REMOVED
#PRINT TARGETS
        INode1_target = INode1.copy()
        INode1_target.move_to([0.27692307692307694, 0.18461538461538463, 0.0])

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
#PRINT ANIMS
        self.play(Transform(INode1, INode1_target))
#PRINT ADDED
#PRINT REMOVED
#PRINT TARGETS
        INode1_target = INode1.copy()
        INode1_target.move_to([-6.1230769230769235, 0.3076923076923077, 0.0])
        INode2_target = INode2.copy()
        INode2_target.move_to([2.784615384615385, -1.2923076923076924, 0.0])
        INode2_target.set_color("#c17d11")

#PRINT MOBJ FUNCS
#PRINT TARGET ADD
#PRINT ANIMS
        self.play(Transform(INode1, INode1_target), Transform(INode2, INode2_target))

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

