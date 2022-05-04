from manim import *
import html
import models.mobject_helper as mh

class IMobject:
    def __init__(self, mobject, parentImobject=None):
        self.mobject = mobject
        self.addedState = None 
        self.removedState = None
        self.introAnim = None
        self.movable = True
        self.isDeleted = False
        self.parentImobject = parentImobject
        self.captured = False

    def copyWith(self, mobject):
        return IMobject(mobject)

class ICircle(IMobject):
    def __init__(self, color=RED, radius=None, parentImobject=None):
        super().__init__(Circle(color=color, radius=radius), parentImobject=parentImobject)
        

    def copyWith(self, mobject):
        return ICircle(mobject)


class ISquare(IMobject):
    def __init__(self):
        super().__init__(Square())

    def copyWith(self, mobject):
        return ISquare(mobject)


class IStar(IMobject):
    def __init__(self):
        super().__init__(Star())

class ITriangle(IMobject):
    def __init__(self):
        super().__init__(Triangle())

class IRegularPolygon(IMobject):
    def __init__(self, n=5):
        super().__init__(RegularPolygon(n))


class IText(IMobject):
    def __init__(self, text, parentImobject=None):
        self.label = Text(text)
        super().__init__(self.label, parentImobject=parentImobject)

        self.label.set_color(RED)
        self.text = text

    def copyWith(self, mobject):
        pass

class IMarkupText(IMobject):
    def __init__(self, text, parentImobject=None, font_size=12, state_handler=None):
        self.label = MarkupText(self.formatText(text), font_size=font_size)
        super().__init__(self.label, parentImobject=parentImobject)

        self.label.set_color(GREY_B)
        self.text = text
        self.state_handler = state_handler
        self.font_size = font_size

    def formatText(self, text):
        return '<span font_family="Consolas">{}</span>'.format(html.escape(text))

    def changeText(self, new_text_str):
        curr_state = self.state_handler.curr

        # create new text
        new_text = MarkupText(self.formatText(new_text_str), font_size=self.font_size)
        new_text.match_color(mh.getCopy(self))
        new_text.move_to(mh.getCopy(self).get_center())

        # configure transforms
        self.state_handler.capture_prev(mh.getCopy(self))
        curr_state.targets[self] = new_text
        curr_state.addTransform(self)

        # setup current ui
        self.state_handler.scene_handler.playCopy(curr_state.getTransform(self), curr_state)

        # update field
        self.text = new_text_str


