import html
from manim import *
from intermediate.imobject import IMobject
import models.mobject_helper as mh
from enum import Enum

class Highlight(Enum):
    BOLD = 1
    ITALICS = 2
    UNDERLINE = 3
    COLOR_CHANGE = 4
    BIG = 5

class IText(IMobject):
    def __init__(self, text, parentImobject=None):
        self.label = Text(text)
        super().__init__(self.label, parentImobject=parentImobject)

        self.label.set_color(RED)
        self.text = text

    def copyWith(self, mobject):
        pass

class IMathTex(IMobject):
    def __init__(self, text, parentImobject=None, font_size=50, fsm_model=None):
        self.text = text
        self.fsm_model = fsm_model
        self.font_size = font_size
        self.label = MathTex(r"{}".format(text), font_size=font_size)
        self.label.set_color(WHITE)
        super().__init__(self.label, parentImobject=parentImobject)

    def changeText(self, new_text_str):
        # update field
        self.text = new_text_str
        curr_state = self.fsm_model.curr
        
        # create new text
        try:
            new_text = MathTex(r"{}".format(new_text_str), font_size=self.font_size, font="Consolas")
            # new_text.match_color(mh.getCopy(self))
            new_text.move_to(mh.getCopy(self).get_center())

            # configure transforms
            self.fsm_model.curr.capture_prev(mh.getCopy(self))
            curr_state.targets[self] = new_text
            curr_state.addTransform(self)

            # setup current ui
            curr_state.playCopy(curr_state.getTransform(self), self.fsm_model.scene_model.scene)
        except:
            print("latex compile error")

class IMarkupText(IMobject):
    def __init__(self, text, parentImobject=None, font_size=14, fsm_model=None):
        self.text = text
        self.fsm_model = fsm_model
        self.font_size = font_size
        self.boldAreas = []
        self.highlight = Highlight.BOLD
        self.label = MarkupText(self.formatText(text), font_size=font_size, font="Consolas")
        self.label.set_color(WHITE)
        super().__init__(self.label, parentImobject=parentImobject)


    def handleBold(self, cs, ce, highlight):
        self.highlight = highlight
        # [(1,3), (4,5) (6,2)]
        # (4, 4)
        newBoldAreas = [(cs, ce)] 
        i = 0
        # while i < len(self.boldAreas):
        #     bs, be = self.boldAreas[i]
        #     if cs > be:
        #         newBoldAreas.append((bs, be))
        #     else:
        #         break

        # if i < len(newBoldAreas) and ce >= bs:
        #     newBoldAreas.append((cs, max(be, ce)))
        #     i += 1
        # else:
        #     newBoldAreas.append((cs, ce))

        # for j in range(i, len(self.boldAreas)):
        #     newBoldAreas.append((bs, be))


        # for bs, be in self.boldAreas:
        #     if cs > be:
        #         newBoldAreas.append((bs, be))
        #         continue

        #     # lbe <= cs <= be
        #     # if ce < bs then insert new before current bold area
        #     # otherwise merge
        #     if ce < bs:
        #         newBoldAreas.append((cs, ce))
        #         newBoldAreas.append((bs, be))
        #     else:
        #         newBoldAreas.append((cs, max(be, ce)))
        
        # print(newBoldAreas)

        self.fsm_model.curr.revAttributes[self]['boldAreas'] = self.boldAreas
        self.fsm_model.curr.changedMobjectAttributes[self]['boldAreas'] = newBoldAreas

        self.boldAreas = newBoldAreas
        # print(self.formatBolds(html.escape(self.text)))
        self.updateMarkupText(self.formatText(self.text))

    def getHighlightTags(self):
        match self.highlight:
            case Highlight.BOLD:
                return '<b>', '</b>'
            case Highlight.UNDERLINE:
                return '<u>', '</u>'
            case Highlight.ITALICS:
                return '<i>', '</i>'
            case Highlight.BIG:
                return '<big>', '</big>'
            case Highlight.COLOR_CHANGE:
                return '<span foreground="#FF0000">', '</span>'
                
    def formatBolds(self, html_text_arr):
        res = []
        curr = 0
        tags, tage = self.getHighlightTags()
        for start, end in self.boldAreas:
            res.extend(html_text_arr[curr:start])
            res.append(tags)
            res.extend(html_text_arr[start:end])
            res.append(tage)
            curr = end
        res.extend(html_text_arr[curr:])
        return res
        
    def formatText(self, text):
        text_arr = list(text)
        html_text_arr = list(map(html.escape, text_arr))
        bolded_text_arr = self.formatBolds(html_text_arr)
        res = ''.join(bolded_text_arr)
        # print(res)
        return res

    def changeText(self, new_text_str):
        # update field
        self.text = new_text_str

        self.updateMarkupText(self.formatText(new_text_str))

        

    def updateMarkupText(self, markupText):
        curr_state = self.fsm_model.curr
        
        # create new text
        new_text = MarkupText(markupText, font_size=self.font_size, font="Consolas")
        # new_text.match_color(mh.getCopy(self))
        new_text.move_to(mh.getCopy(self).get_center())

        # configure transforms
        self.fsm_model.curr.capture_prev(mh.getCopy(self))
        curr_state.targets[self] = new_text
        curr_state.addTransform(self)

        # setup current ui
        curr_state.playCopy(curr_state.getTransform(self), self.fsm_model.scene_model.scene)

        self.editedAt = curr_state.idx