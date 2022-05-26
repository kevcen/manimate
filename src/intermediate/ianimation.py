import models.mobject_helper as mh

class IAnimation:
    def __init__(self, imobject):
        self.imobject = imobject

class IFadeIn(IAnimation):
    pass

class ITransform(IAnimation):
    pass

class ICreate(IAnimation):
    pass

class IApplyMethod(IAnimation):
    def __init__(self, imobject):
        self.imobject = imobject
        self.color = None
        self.move_to = None
        self.scale = None

    def custom_method(self, mobject):
        if self.color is not None:
            mobject.set_color(self.color)
        if self.move_to is not None:
            mobject.move_to(self.move_to)
        if self.scale is not None:
            mobject.scale(self.scale)
            
        return mobject