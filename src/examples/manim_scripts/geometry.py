from manim import *

class Main(Scene):
    def construct(self):
        self.wait(1.0)

        description = MarkupText("""here we look at the properties of different <span foreground=\"#e9b96e\">geometrical</span> shapes""", font_size=21, font="Consolas")
        self.play(Create(description))

        title = MarkupText("""Geometry""", font_size=56, font="Consolas")
        title.set_color("#e9b96e")
        self.play(ReplacementTransform(description, title))

        circle = Circle(color="#FC6255", radius=None)
        circle.move_to([0.015384615384615385, 1.9230769230769231, 0.0])
        circle.set_color("#e9b96e")
        area_text = MarkupText("""this <span foreground=\"#e9b96e\">circle</span> has area:""", font_size=14, font="Consolas")
        area_text.move_to([-1.9846153846153842, -0.47692307692307695, 0.0])
        self.play(ReplacementTransform(title, circle), Create(area_text))

        area_formula = MathTex(r"A = \\pi r ^ 2", font_size=40)
        area_formula.move_to([2.153846153846154, -0.46153846153846145, -1.5407439555097887e-33])
        area_formula.set_color("#729fcf")
        self.play(FadeIn(area_formula))

        perimeter_text = MarkupText("""and perimeter:""", font_size=14, font="Consolas")
        perimeter_text.move_to([-1.6307692307692305, -1.8153846153846152, 0.0])
        perimeter_formula = MathTex(r"P = 2\\pi r", font_size=40)
        perimeter_formula.move_to([2.1076923076923078, -1.7692307692307696, -1.5407439555097887e-33])
        perimeter_formula.set_color("#fc6255")
        self.play(Create(perimeter_text), FadeIn(perimeter_formula))
        self.wait(1.0)

        square = Square()
        square.move_to([0.015384615384615385, 1.9230769230769231, 0.0])
        square.set_color("#e9b96e")
        area_text_square = MarkupText("""this <span foreground=\"#e9b96e\">square</span> has area:""", font_size=14, font="Consolas")
        area_text_square.move_to([-1.9846153846153842, -0.47692307692307695, 0.0])
        area_formula_square = MathTex(r"A = l ^ 2", font_size=40)
        area_formula_square.set_color("#729fcf")
        area_formula_square.move_to([2.153846153846154, -0.46153846153846145, -1.5407439555097887e-33])
        perimeter_formula_square = MathTex(r"P = 4l", font_size=40)
        perimeter_formula_square.set_color("#fc6255")
        perimeter_formula_square.move_to([2.1076923076923078, -1.7692307692307696, -1.5407439555097887e-33])
        self.play(ReplacementTransform(circle, square), Transform(area_text, area_text_square), Transform(area_formula, area_formula_square), Transform(perimeter_formula, perimeter_formula_square))
        self.wait(4)

        triangle = Triangle()
        triangle.move_to([0.015384615384615385, 1.9230769230769231, 0.0])
        triangle.set_color("#e9b96e")
        area_text_triangle = MarkupText("""this <span foreground=\"#e9b96e\">triangle</span> has area:""", font_size=14, font="Consolas")
        area_text_triangle.move_to([-1.9846153846153842, -0.4769230769230769, 0.0])
        area_formula_triangle = MathTex(r"A = \\frac{1}{2} b h", font_size=40)
        area_formula_triangle.set_color("#729fcf")
        area_formula_triangle.move_to([2.153846153846154, -0.46153846153846145, -1.5407439555097887e-33])
        perimeter_formula_square = MathTex(r"P = 3b", font_size=40)
        perimeter_formula_square.set_color("#fc6255")
        perimeter_formula_square.move_to([2.1076923076923078, -1.7692307692307696, -1.5407439555097887e-33])
        self.play(ReplacementTransform(square, triangle), Transform(area_text, area_text_triangle), Transform(area_formula, area_formula_triangle), Transform(perimeter_formula, perimeter_formula_square))
        self.wait(4)