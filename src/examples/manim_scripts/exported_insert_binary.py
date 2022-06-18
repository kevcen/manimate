from manim import *

class Main(Scene):
    def construct(self):
        self.wait(1.0)
        IMarkupText2 = MarkupText("""inserting into a binary tree""", font_size=14, font="Consolas")
        IMarkupText2.move_to([0.0, 0.0, 0.0])

        self.play(Create(IMarkupText2))
        INode0 = Tree("5", parent=None)
        INode1 = Tree("3", parent=INode0)
        INode2 = Tree("1", parent=INode1)
        INode3 = Tree("4", parent=INode1)
        INode4 = Tree("8", parent=INode0)
        INode5 = Tree("6", parent=INode4)
        INode6 = Tree("9", parent=INode4)
        IText0 = INode0.label
        IText1 = INode1.label
        IText2 = INode2.label
        IText3 = INode3.label
        IText4 = INode4.label
        IText5 = INode5.label
        IText6 = INode6.label
        INode0.move_to([0.0884389759495341, 2.9384615384615387, 0.0])
        INode1.move_to([-3.5555555555555554, 0.6256410256410256, 0.0])
        INode2.move_to([-5.333333333333333, -1.6871794871794874, 0.0])
        INode3.move_to([-1.7777777777777777, -1.6871794871794874, 0.0])
        INode4.move_to([3.5555555555555554, 0.6256410256410256, 0.0])
        INode5.move_to([1.7777777777777777, -1.6871794871794874, 0.0])
        INode6.move_to([5.333333333333333, -1.6871794871794874, 0.0])
        IText0.move_to([0.0884389759495341, 2.9384615384615387, 0.0])
        IText1.move_to([-3.5555555555555554, 0.6256410256410256, 0.0])
        IText2.move_to([-5.333333333333333, -1.6871794871794874, 0.0])
        IText3.move_to([-1.7777777777777777, -1.6871794871794874, 0.0])
        IText4.move_to([3.5555555555555554, 0.6256410256410256, 0.0])
        IText5.move_to([1.7777777777777777, -1.6871794871794874, 0.0])
        IText6.move_to([5.333333333333333, -1.6871794871794874, 0.0])
        IParentEdge0 = ParentEdge(INode1)
        IParentEdge1 = ParentEdge(INode2)
        IParentEdge2 = ParentEdge(INode3)
        IParentEdge3 = ParentEdge(INode4)
        IParentEdge4 = ParentEdge(INode5)
        IParentEdge5 = ParentEdge(INode6)

        self.play(FadeIn(INode0), FadeIn(INode1), FadeIn(IParentEdge0), FadeIn(INode4), FadeIn(IParentEdge3), FadeIn(INode6), FadeIn(IParentEdge5), FadeIn(INode5), FadeIn(IParentEdge4), FadeIn(INode3), FadeIn(IParentEdge2), FadeIn(INode2), FadeIn(IParentEdge1))
        self.remove(IMarkupText2)

        INode7 = Tree("7", parent=None)
        IText7 = INode7.label
        INode7.move_to([-5.1577148702043125, 2.815384615384615, 0.0])
        INode7.set_color("#ad7fa8")
        IText7.move_to([-5.1577148702043125, 2.815384615384615, 0.0])

        self.play(FadeIn(INode7))
        INode7_target = INode7.copy()
        INode0_target = INode0.copy()
        IMathTex0 = MathTex(r"{}".format("<"), font_size=50)
        INode7_target.move_to([2.1192082067187643, 2.815384615384615, 0.0])
        INode7_target.set_color("#ad7fa8")
        INode0_target.set_color("#fce94f")
        IMathTex0.move_to([1.153846153846154, 2.8000000000000003, -1.5407439555097887e-33])
        IMathTex0.set_color("#ffffff")

        self.play(Transform(INode0, INode0_target), Transform(INode7, INode7_target), FadeIn(IMathTex0))
        INode7_target = INode7.copy()
        INode4_target = INode4.copy()
        INode0_target = INode0.copy()
        IMathTex0_target = MathTex(r"{}".format(">"), font_size=50)
        INode7_target.move_to([5.16536205287261, 1.2307692307692306, 0.0])
        INode4_target.set_color("#fce94f")
        INode0_target.set_color("#fc6255")
        IMathTex0_target.move_to([4.246153846153846, 1.1076923076923075, -1.5407439555097887e-33])
        IMathTex0_target.set_color("#ffffff")

        self.play(Transform(INode0, INode0_target), Transform(INode4, INode4_target), Transform(INode7, INode7_target), Transform(IMathTex0, IMathTex0_target))
        INode7_target = INode7.copy()
        INode5_target = INode5.copy()
        INode4_target = INode4.copy()
        IMathTex0_target = MathTex(r"{}".format("<"), font_size=50)
        INode7_target.move_to([0.011515899026455945, -1.6000000000000003, 0.0])
        INode5_target.set_color("#fce94f")
        INode4_target.set_color("#fc6255")
        IMathTex0_target.move_to([0.9538461538461538, -1.6153846153846156, -1.5407439555097887e-33])
        IMathTex0_target.set_color("#ffffff")

        self.play(Transform(INode4, INode4_target), Transform(INode5, INode5_target), Transform(INode7, INode7_target), Transform(IMathTex0, IMathTex0_target))
        self.remove(IMathTex0)

        INode7_target = INode7.copy()
        INode5_target = INode5.copy()
        INode7_target.move_to([2.811515899026456, -3.0000000000000004, 0.0])
        INode7_target.set_parent(INode5_target)
        INode7_target.set_color("#fc6255")
        INode5_target.set_color("#8ae234")
        IParentEdge6 = ParentEdge(INode7)

        self.add(IParentEdge6)
        self.play(Transform(INode5, INode5_target), Transform(INode7, INode7_target))
        INode5_target = INode5.copy()
        INode1_target = INode1.copy()
        INode2_target = INode2.copy()
        INode3_target = INode3.copy()
        INode4_target = INode4.copy()
        INode6_target = INode6.copy()
        INode7_target = INode7.copy()
        INode5_target.set_color("#fc6255")
        INode5_target.move_to([1.516239316239316, -0.6871794871794874, 0.0])
        INode1_target.move_to([-4.032478632478632, 1.2256410256410257, 0.0])
        INode2_target.move_to([-5.7333333333333325, -0.5641025641025642, 0.0])
        INode3_target.move_to([-1.6700854700854701, -0.594871794871795, 0.0])
        INode4_target.move_to([3.817094017094017, 1.4717948717948717, 0.0])
        INode6_target.move_to([5.825641025641025, -0.641025641025641, 0.0])
        INode7_target.move_to([3.011515899026456, -2.876923076923078, 0.0])

        self.play(Transform(INode7, INode7_target), Transform(INode6, INode6_target), Transform(INode4, INode4_target), Transform(INode3, INode3_target), Transform(INode2, INode2_target), Transform(INode1, INode1_target), Transform(INode5, INode5_target))

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

