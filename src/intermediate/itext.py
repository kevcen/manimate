import html
from manim import *
from intermediate.ianimation import ITransform
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

    def declStr(self):
        return f"Text({self.text})"

class IMathTex(IMobject):
    def __init__(self, text, parentImobject=None, font_size=50, fsm_model=None):
        self.text = text
        self.fsm_model = fsm_model
        self.font_size = font_size
        self.label = MathTex(r"{}".format(text), font_size=font_size, font="Consolas")
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

            if not self.fsm_model.created_at_curr_state(self):
                curr_state.addTransform(self)

            # setup current ui
            curr_state.playCopy(ITransform(self), self.fsm_model.scene_model.scene)

            #store for writer 
            curr_state.targetDeclStr[self] = self.declStr()

        except:
            print("latex compile error")

    def declStr(self):
        return f"MathTex(r\"{{}}\".format(\"{self.text}\"), font_size={self.font_size}, font=\"Consolas\")"

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
        newBoldAreas = [(cs, ce)] 
        
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

        self.fsm_model.curr.revAttributes[self]['text'] = self.text
        self.fsm_model.curr.changedMobjectAttributes[self]['text'] = new_text_str

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

        if not self.fsm_model.created_at_curr_state(self):
            curr_state.addTransform(self)

        #store for writer 
        curr_state.targetDeclStr[self] = self.declStr()

        # setup current ui
        curr_state.playCopy(ITransform(self), self.fsm_model.scene_model.scene)

        self.editedAt = curr_state.idx

    def declStr(self):
        return f"MarkupText(\"{self.formatText(self.text)}\", font_size={self.font_size}, font=\"Consolas\")"