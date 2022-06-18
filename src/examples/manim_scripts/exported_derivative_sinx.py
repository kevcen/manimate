from manim import *

class Main(Scene):
    def construct(self):
        IMarkupText0 = MarkupText("""derive sin(x)""", font_size=14, font="Consolas")
        IMarkupText0.move_to([0.0, 0.0, 0.0])
        IMarkupText0.scale(1.1666666666666667)

        self.play(Create(IMarkupText0))
        IMathTex0 = MathTex(r"{}".format("\\frac{d}{dx} (sin(x))"), font_size=50)
        IMathTex0.move_to([0.0, 0.0, 0.0])
        IMathTex0.set_color("#ffffff")

        self.play(ReplacementTransform(IMarkupText0, IMathTex0))
        IMathTex0_target = IMathTex0.copy()
        IMathTex0_target.move_to([-5.415384615384617, 2.8923076923076927, 0.0])

        self.play(Transform(IMathTex0, IMathTex0_target))
        IMathTex1 = MathTex(r"{}".format("= \\lim_{h\\to0} \\frac{sin(x)cos(h) + cos(x)sin(h) - sin(x)}{h}"), font_size=50)
        IMathTex1.move_to([0.3846153846153848, 2.8923076923076922, 0.0])
        IMathTex1.set_color("#ffffff")
        IMathTex1.scale(0.8)

        self.play(Create(IMathTex1))
        IMarkupText1 = MarkupText("""first principles""", font_size=14, font="Consolas")
        IMarkupText1.move_to([5.76923076923077, 2.7538461538461543, 0.0])
        IMarkupText1.set_color("#fce94f")

        self.play(FadeIn(IMarkupText1))
        IMathTex2 = MathTex(r"{}".format("= \\lim_{h\\to0} \\frac{sin(x)(cos(h)- 1) + cos(x)sin(h)}{h}"), font_size=50)
        IMathTex2.move_to([0.12307692307692253, 1.523076923076922, 0.0])
        IMathTex2.set_color("#ffffff")
        IMathTex2.scale(0.8)

        self.play(Create(IMathTex2))
        IMarkupText2 = MarkupText("""factorising sin(x)""", font_size=14, font="Consolas")
        IMarkupText2.move_to([5.753846153846155, 1.4769230769230766, -1.5407439555097887e-33])
        IMarkupText2.set_color("#fce94f")

        self.play(FadeIn(IMarkupText2))
        IMathTex3 = MathTex(r"{}".format("= \\lim_{h\\to0} [sin(x)\\frac{cos(h)-1}{h} + cos(x)\\frac{sin(h)}{h}]"), font_size=50)
        IMathTex3.move_to([0.09230769230769287, 0.046153846153846156, 3.0814879110195774e-33])
        IMathTex3.set_color("#ffffff")
        IMathTex3.scale(0.8)

        self.play(Create(IMathTex3))
        IMarkupText3 = MarkupText("""factorising f(x)""", font_size=14, font="Consolas")
        IMarkupText3.move_to([5.707692307692308, 0.046153846153846156, 0.0])
        IMarkupText3.set_color("#fce94f")

        self.play(FadeIn(IMarkupText3))
        IMathTex4 = MathTex(r"{}".format("= sin(x)\\lim_{h\\to0} [\\frac{cos(h)-1}{h}] + cos(x)\\lim_{h\\to0} [\\frac{sin(h)}{h}]"), font_size=50)
        IMathTex4.move_to([0.6615384615384619, -1.3846153846153848, 0.0])
        IMathTex4.set_color("#ffffff")
        IMathTex4.scale(0.8)

        self.play(Create(IMathTex4))
        IMarkupText4 = MarkupText("""distribute lim""", font_size=14, font="Consolas")
        IMarkupText4.move_to([6.107692307692307, -1.4923076923076923, 0.0])
        IMarkupText4.set_color("#fce94f")

        self.play(FadeIn(IMarkupText4))
        IMathTex5 = MathTex(r"{}".format("= cos(x)"), font_size=50)
        IMathTex5.move_to([-2.5538461538461545, -2.8769230769230774, -1.5407439555097887e-33])
        IMathTex5.set_color("#ffffff")

        self.play(Create(IMathTex5))
        IMathTex7 = MathTex(r"{}".format("\\lim_{h\\to0} \\frac{sin(h)}{h} = 1"), font_size=50)
        IMathTex7.move_to([5.8307692307692305, -2.7230769230769227, 0.0])
        IMathTex7.set_color("#fce94f")
        IMathTex7.scale(0.5)

        self.play(FadeIn(IMathTex7))
        self.wait(1.0)
