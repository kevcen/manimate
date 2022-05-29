from manim import *

class Main(Scene):
    def construct(self):

        IMarkupText0 = MarkupText("hi", font_size=14, font="Consolas")
        IMarkupText0.move_to([-2.876923076923077, -0.47692307692307695, 0.0])
        self.add(IMarkupText0)

        self.wait(1)
        IMarkupText0_target = MarkupText("hi everyone", font_size=14, font="Consolas")
        IMarkupText0_target.move_to([-2.753846153846154, -0.5076923076923077, 0.0])

        self.play(Transform(IMarkupText0, IMarkupText0_target))
        IMarkupText0_target = MarkupText("hi everyone its ok", font_size=14, font="Consolas")
        IMarkupText0_target.move_to([-2.4615384615384617, -0.35384615384615387, 0.0])

        self.play(Transform(IMarkupText0, IMarkupText0_target))
        IMarkupText0_target = MarkupText("hi everyone its <big>ok</big>", font_size=14, font="Consolas")
        IMarkupText0_target.move_to([-3.030769230769231, -0.27692307692307694, 0.0])

        self.play(Transform(IMarkupText0, IMarkupText0_target))
