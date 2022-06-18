from manim import *

class Main(Scene):
    def construct(self):
        self.wait(1.0)

        description = MarkupText("""inserting into a binary tree""", font_size=14, font="Consolas")
        self.play(Create(description))

        node5 = Tree("5", parent=None)
        node5.move_to([0.0884389759495341, 2.9384615384615387, 0.0])
        node3 = Tree("3", parent=node5)
        node3.move_to([-3.5555555555555554, 0.6256410256410256, 0.0])
        node1 = Tree("1", parent=node3)
        node1.move_to([-5.333333333333333, -1.6871794871794874, 0.0])
        node4 = Tree("4", parent=node3)
        node4.move_to([-1.7777777777777777, -1.6871794871794874, 0.0])
        node8 = Tree("8", parent=node5)
        node8.move_to([3.5555555555555554, 0.6256410256410256, 0.0])
        node6 = Tree("6", parent=node8)
        node6.move_to([1.7777777777777777, -1.6871794871794874, 0.0])
        node9 = Tree("9", parent=node8)
        node9.move_to([5.333333333333333, -1.6871794871794874, 0.0])
        parent_edge_3 = ParentEdge(node3)
        parent_edge_1 = ParentEdge(node1)
        parent_edge_4 = ParentEdge(node4)
        parent_edge_8 = ParentEdge(node8)
        parent_edge_6 = ParentEdge(node6)
        parent_edge_9 = ParentEdge(node9)
        self.play(FadeIn(node5), FadeIn(node3), FadeIn(parent_edge_3), FadeIn(node8), FadeIn(parent_edge_8), FadeIn(node9), FadeIn(parent_edge_9), FadeIn(node6), FadeIn(parent_edge_6), FadeIn(node4), FadeIn(parent_edge_4), FadeIn(node1), FadeIn(parent_edge_1))
        self.remove(description)

        node7 = Tree("7", parent=None)
        node7.move_to([-5.1577148702043125, 2.815384615384615, 0.0])
        node7.set_color("#ad7fa8")
        self.play(FadeIn(node7))

        node7.generate_target()
        node7.target.move_to([2.1192082067187643, 2.815384615384615, 0.0])
        node7.target.set_color("#ad7fa8")
        node5.generate_target()
        node5.target.set_color("#fce94f")
        inequality = MathTex(r"<", font_size=50)
        inequality.move_to([1.153846153846154, 2.8000000000000003, -1.5407439555097887e-33])
        inequality.set_color("#ffffff")
        self.play(Transform(node5, node5.target), Transform(node7, node7.target), FadeIn(inequality))

        node7.generate_target()
        node7.target.move_to([5.16536205287261, 1.2307692307692306, 0.0])
        node8.generate_target()
        node8.target.set_color("#fce94f")
        node5.generate_target()
        node5.target.set_color("#fc6255")
        inequality_target = MathTex(r">", font_size=50)
        inequality_target.move_to([4.246153846153846, 1.1076923076923075, -1.5407439555097887e-33])
        inequality_target.set_color("#ffffff")
        self.play(Transform(node5, node5.target), Transform(node8, node8.target), Transform(node7, node7.target), Transform(inequality, inequality_target))
        
        node7.generate_target()
        node7.target.move_to([0.011515899026455945, -1.6000000000000003, 0.0])
        node6.generate_target()
        node6.target.set_color("#fce94f")
        node8.generate_target()
        node8.target.set_color("#fc6255")
        inequality_target = MathTex(r"<", font_size=50)
        inequality_target.move_to([0.9538461538461538, -1.6153846153846156, -1.5407439555097887e-33])
        inequality_target.set_color("#ffffff")
        self.play(Transform(node8, node8.target), Transform(node6, node6.target), Transform(node7, node7.target), Transform(inequality, inequality.target))
        self.remove(inequality)

        node7.generate_target()
        node7.target.move_to([2.811515899026456, -3.0000000000000004, 0.0])
        node7.target.set_parent(node6.target)
        node7.target.set_color("#fc6255")
        node6.generate_target()
        node6.target.set_color("#8ae234")
        IParentEdge6 = ParentEdge(node7)
        self.add(IParentEdge6)
        self.play(Transform(node6, node6.target), Transform(node7, node7.target))

        node6.generate_target()
        node6.target.set_color("#fc6255")
        node6.target.move_to([1.516239316239316, -0.6871794871794874, 0.0])
        node3.generate_target()
        node3.target.move_to([-4.032478632478632, 1.2256410256410257, 0.0])
        node1.generate_target()
        node1.target.move_to([-5.7333333333333325, -0.5641025641025642, 0.0])
        node4.generate_target()
        node4.target.move_to([-1.6700854700854701, -0.594871794871795, 0.0])
        node8.generate_target()
        node8.target.move_to([3.817094017094017, 1.4717948717948717, 0.0])
        node9.generate_target()
        node9.target.move_to([5.825641025641025, -0.641025641025641, 0.0])
        node7.generate_target()
        node7.target.move_to([3.011515899026456, -2.876923076923078, 0.0])
        self.play(Transform(node7, node7.target), Transform(node9, node9.target), Transform(node8, node8.target), Transform(node4, node4.target), Transform(node1, node1.target), Transform(node3, node3.target), Transform(node6, node6.target))

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

