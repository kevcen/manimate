import html
from enum import Enum
from manim import *
from intermediate.ianimation import ITransform
from intermediate.imobject import IMobject
import controllers.mobject_helper as mh


class Highlight(Enum):
    """
    Type of highlights that can be done of MarkupText
    """

    BOLD = 1
    ITALICS = 2
    UNDERLINE = 3
    COLOR_CHANGE = 4
    BIG = 5


class IText(IMobject):
    """
    Intermediate Text mobject
    """

    def __init__(self, text, parent_imobject=None):
        self.label = Text(text)
        super().__init__(self.label, parent_imobject=parent_imobject)

        self.label.set_color(RED)
        self.text = text

    def decl_str(self):
        return f"Text({self.text})"


class IMathTex(IMobject):
    """
    Intermediate MathTex mobject
    """

    def __init__(self, text, parent_imobject=None, font_size=50, fsm_controller=None):
        self.text = text
        self.fsm_controller = fsm_controller
        self.font_size = font_size
        self.label = MathTex(r"{}".format(text), font_size=font_size)
        self.label.set_color("#FFFFFF")
        super().__init__(self.label, parent_imobject=parent_imobject)

    def change_text(self, new_text_str):
        # update field
        curr_state = self.fsm_controller.curr
        # create new text
        try:
            new_text = MathTex(r"{}".format(new_text_str), font_size=self.font_size)

            new_text.match_color(mh.get_copy(self))  # selected color
            new_text.move_to(mh.get_copy(self).get_center())

            # configure transforms
            self.fsm_controller.curr.capture_prev(mh.get_copy(self))
            curr_state.targets[self] = new_text

            if mh.get_copy(self) in self.fsm_controller.scene_controller.selected:
                color = self.fsm_controller.scene_controller.selected[mh.get_copy(self)]
                curr_state.targets[self].set_color(color)
            # store for writer
            self.text = new_text_str
            self.fsm_controller.edit_transform_target(
                self,
                new_text.copy(),
                color=color,
                move_to=mh.get_copy(self).get_center().tolist(),
            )
            curr_state.target_decl_str[self] = self.decl_str()

            # setup current ui
            curr_state.play_copy(
                ITransform(self), self.fsm_controller.scene_controller.scene
            )
        except Exception as e:
            print(e)
            if self.text != new_text_str:
                return (
                    f"Cannot compile {new_text_str} into latex.",
                    None,
                )

        return None

    def decl_str(self):
        text = self.text.replace('\\', '\\\\')
        return f'MathTex(r"{{}}".format("{text}"), font_size={self.font_size})'


class IMarkupText(IMobject):
    """
    Intermediate MarkupText mobject
    """

    def __init__(self, text, parent_imobject=None, font_size=14, fsm_controller=None):
        self.text = text
        self.fsm_controller = fsm_controller
        self.font_size = font_size
        self.bold_areas = []
        self.highlight = Highlight.BOLD
        self.bold_color = RED
        self.label = MarkupText(
            self.format_text(text), font_size=font_size, font="Consolas"
        )
        self.label.set_color(WHITE)
        super().__init__(self.label, parent_imobject=parent_imobject)

    def handle_bold(self, cs, ce, highlight):
        self.highlight = highlight
        new_bold_areas = [(cs, ce)]

        if "bold_areas" not in self.fsm_controller.curr.rev_attributes[self]:
            self.fsm_controller.curr.rev_attributes[self][
                "bold_areas"
            ] = self.bold_areas
        self.fsm_controller.curr.changed_mobject_attributes[self][
            "bold_areas"
        ] = new_bold_areas

        self.bold_areas = new_bold_areas

        # print(self.format_bolds(html.escape(self.text)))
        self.update_markup_text(self.format_text(self.text))

    def clear_bold(self):
        if "bold_areas" not in self.fsm_controller.curr.rev_attributes[self]:
            self.fsm_controller.curr.rev_attributes[self][
                "bold_areas"
            ] = self.bold_areas
        self.fsm_controller.curr.changed_mobject_attributes[self]["bold_areas"] = []

        self.bold_areas = []
        self.update_markup_text(self.format_text(self.text))

    def get_highlight_tags(self):
        match self.highlight:
            case Highlight.BOLD:
                return "<b>", "</b>"
            case Highlight.UNDERLINE:
                return "<u>", "</u>"
            case Highlight.ITALICS:
                return "<i>", "</i>"
            case Highlight.BIG:
                return "<big>", "</big>"
            case Highlight.COLOR_CHANGE:
                return f'<span foreground="{self.bold_color}">', "</span>"

    def format_bolds(self, html_text_arr):
        res = []
        curr = 0
        tags, tage = self.get_highlight_tags()
        for start, end in self.bold_areas:
            res.extend(html_text_arr[curr:start])
            res.append(tags)
            res.extend(html_text_arr[start:end])
            res.append(tage)
            curr = end
        res.extend(html_text_arr[curr:])
        return res

    def format_text(self, text):
        text_arr = list(text)
        html_text_arr = list(map(html.escape, text_arr))
        bolded_text_arr = self.format_bolds(html_text_arr)
        res = "".join(bolded_text_arr)
        # print(res)
        return res

    def change_text(self, new_text_str):
        # update field
        if "text" not in self.fsm_controller.curr.rev_attributes[self]:
            self.fsm_controller.curr.rev_attributes[self]["text"] = self.text
        self.fsm_controller.curr.changed_mobject_attributes[self]["text"] = new_text_str

        self.text = new_text_str

        self.update_markup_text(self.format_text(new_text_str))
        return None

    def update_markup_text(self, markup_text):
        curr_state = self.fsm_controller.curr

        # create new text
        new_text = MarkupText(markup_text, font_size=self.font_size, font="Consolas")
        # new_text.match_color(mh.getCopy(self))
        new_text.scale(self.past_scale)
        new_text.move_to(mh.get_copy(self).get_center())

        # configure transforms
        self.fsm_controller.curr.capture_prev(mh.get_copy(self))
        curr_state.targets[self] = new_text

        # store for writer
        self.fsm_controller.edit_transform_target(
            self,
            new_text,
            move_to=mh.get_copy(self).get_center().tolist(),
            scale=self.past_scale,
        )
        curr_state.target_decl_str[self] = self.decl_str()

        # setup current ui
        curr_state.play_copy(
            ITransform(self), self.fsm_controller.scene_controller.scene
        )

    def decl_str(self):
        print("markup delc  str")
        text = self.format_text(self.text).replace('"', '\\"')
        return f'MarkupText("""{text}""", font_size={self.font_size}, font="Consolas")'
