from manim import *

class Main(Scene):
    def construct(self):
        derive_question = MarkupText("""derive sin(x)""", font_size=16, font="Consolas")

        self.play(Create(derive_question))
        dydx = MathTex(r"\\frac{d}{dx} (sin(x))", font_size=50)

        self.play(ReplacementTransform(derive_question, dydx))
        dydx.generate_target()
        dydx.target.move_to([-5.415384615384617, 2.8923076923076927, 0.0])

        self.play(Transform(dydx, dydx.target))
        lim_1 = MathTex(r"{}".format("= \\lim_{h\\to0} \\frac{sin(x)cos(h) + cos(x)sin(h) - sin(x)}{h}"), font_size=40)
        lim_1.move_to([0.3846153846153848, 2.8923076923076922, 0.0])

        self.play(Create(lim_1))
        description_1 = MarkupText("""first principles""", font_size=14, font="Consolas")
        description_1.move_to([5.76923076923077, 2.7538461538461543, 0.0])
        description_1.set_color("#fce94f")

        self.play(FadeIn(description_1))
        lim_2 = MathTex(r"{}".format("= \\lim_{h\\to0} \\frac{sin(x)(cos(h)- 1) + cos(x)sin(h)}{h}"), font_size=40)
        lim_2.move_to([0.12307692307692253, 1.523076923076922, 0.0])

        self.play(Create(lim_2))
        description_2 = MarkupText("""factorising sin(x)""", font_size=14, font="Consolas")
        description_2.move_to([5.753846153846155, 1.4769230769230766, -1.5407439555097887e-33])
        description_2.set_color("#fce94f")

        self.play(FadeIn(description_2))
        lim_3 = MathTex(r"{}".format("= \\lim_{h\\to0} [sin(x)\\frac{cos(h)-1}{h} + cos(x)\\frac{sin(h)}{h}]"), font_size=40)
        lim_3.move_to([0.09230769230769287, 0.046153846153846156, 3.0814879110195774e-33])

        self.play(Create(lim_3))
        description_3 = MarkupText("""factorising f(x)""", font_size=14, font="Consolas")
        description_3.move_to([5.707692307692308, 0.046153846153846156, 0.0])

        self.play(FadeIn(description_3))
        lim_4 = MathTex(r"{}".format("= sin(x)\\lim_{h\\to0} [\\frac{cos(h)-1}{h}] + cos(x)\\lim_{h\\to0} [\\frac{sin(h)}{h}]"), font_size=40)
        lim_4.move_to([0.6615384615384619, -1.3846153846153848, 0.0])

        self.play(Create(lim_4))
        description_4 = MarkupText("""distribute lim""", font_size=14, font="Consolas")
        description_4.move_to([6.107692307692307, -1.4923076923076923, 0.0])
        description_4.set_color("#fce94f")

        self.play(FadeIn(description_4))
        answer = MathTex(r"{}".format("= cos(x)"), font_size=50)
        answer.move_to([-2.5538461538461545, -2.8769230769230774, -1.5407439555097887e-33])

        self.play(Create(answer))
        description_5 = MathTex(r"{}".format("\\lim_{h\\to0} \\frac{sin(h)}{h} = 1"), font_size=25)
        description_5.move_to([5.8307692307692305, -2.7230769230769227, 0.0])
        description_5.set_color("#fce94f")

        self.play(FadeIn(description_5))
        self.wait(1.0)
