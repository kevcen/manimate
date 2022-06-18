from manim import *

class CoolChart(VGroup):
    def __init__(self):
        # the location of the ticks depends on the x_range and y_range.
        grid = Axes(
            x_range=[0, 1, 0.05],  # step size determines num_decimal_places.
            y_range=[0, 1, 0.05],
            x_length=9,
            y_length=5.5,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.1),
                "font_size": 24,
            },
            tips=False,
        )

        # Labels for the x-axis and y-axis.
        y_label = grid.get_y_axis_label("y", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = grid.get_x_axis_label("x")
        grid_labels = VGroup(x_label, y_label)

        graphs = VGroup()
        for n in np.arange(1, 20 + 0.5, 0.5):
            graphs += grid.plot(lambda x: x ** n, color=WHITE)
            graphs += grid.plot(
                lambda x: x ** (1 / n), color=WHITE, use_smoothing=False
            )

        # Extra lines and labels for point (1,1)
        graphs += Dot(point=grid.c2p(1, 1, 0), color=YELLOW)
        graphs += Tex("(1,1)").scale(0.75).next_to(grid.c2p(1, 1, 0))
        title = Title(
            # spaces between braces to prevent SyntaxError
            r"Graphs of $y=x^{ {1}\over{n} }$ and $y=x^n (n=1,2,3,...,20)$",
            include_underline=False,
            font_size=40,
        )
        super().__init__(title, graphs, grid, grid_labels)

class PolarChart(VGroup):
    def __init__(self):
        polarplane_pi = PolarPlane(
            azimuth_units="PI radians",
            size=6,
            azimuth_label_font_size=33.6,
            radius_config={"font_size": 33.6},
        ).add_coordinates()
        super().__init__(polarplane_pi)


class SmallNumberLine(NumberLine):
    def __init__(self):
        super().__init__(
            x_range=[-10, 10, 2],
            length=10,
            color=BLUE,
            include_numbers=True,
            label_direction=UP,
        )

class DoCTable(Table):
	def __init__(self):
		super().__init__(
            [["88", "14"], ["20", "8"]],
            row_labels=[Text("Male"), Text("Female")],
            col_labels=[Text("Students"), Text("Lecturers")],
        )


class NaughtsAndCrosses(MobjectTable):
    def __init__(self):
        cross = VGroup(Line(UP + LEFT, DOWN + RIGHT), Line(UP + RIGHT, DOWN + LEFT))
        a = Circle().scale(0.5)
        b = cross.scale(0.5)
        super().__init__(
            [
                [a.copy(), b.copy(), a.copy()],
                [b.copy(), a.copy(), a.copy()],
                [a.copy(), b.copy(), b.copy()],
            ]
        )