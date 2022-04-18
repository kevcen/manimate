from manim import *

class Main(Scene):
  def construct(self):
    Circle0 = Circle()

    Circle1 = Circle()

    Circle2 = Circle()

    Circle3 = Circle()

    self.play(Create(Circle0), Create(Circle1), Create(Circle2), Create(Circle3))
    Circle4 = Circle()
    Circle4.move_to([3.36, 0.128, 0.0])

    Circle5 = Circle()
    Circle5.move_to([2.0, -2.688, 0.0])

    Circle6 = Circle()
    Circle6.move_to([-2.912, -0.592, 0.0])

    Circle7 = Circle()
    Circle7.move_to([-2.32, 1.792, 0.0])

    self.play(Transform(Circle3, Circle4), Transform(Circle2, Circle5), Transform(Circle1, Circle6), Transform(Circle0, Circle7))
    Circle8 = Circle()
    Circle8.move_to([6.352, 1.824, 0.0])

    Circle9 = Circle()
    Circle9.move_to([-4.368, -1.76, 0.0])

    Circle10 = Circle()
    Circle10.move_to([4.864, -1.84, 0.0])

    Circle11 = Circle()
    Circle11.move_to([-3.52, 1.6320000000000001, 0.0])

    Square0 = Square()

    self.play(Transform(Circle1, Circle8), Transform(Circle3, Circle9), Transform(Circle0, Circle10), Transform(Circle2, Circle11), Create(Square0))
    Square1 = Square()
    Square1.move_to([3.584, 1.536, 0.0])

    Circle12 = Circle()
    Circle12.move_to([1.9040000000000001, -2.352, 0.0])

    Circle13 = Circle()
    Circle13.move_to([-4.5280000000000005, 1.856, 0.0])

    Circle14 = Circle()
    Circle14.move_to([5.808, -0.736, 0.0])

    Circle15 = Circle()
    Circle15.move_to([-4.144, -2.384, 0.0])

    self.play(Transform(Square0, Square1), Transform(Circle2, Circle12), Transform(Circle0, Circle13), Transform(Circle3, Circle14), Transform(Circle1, Circle15))
    self.wait(1)
