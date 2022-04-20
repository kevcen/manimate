

class IAnimation:
    def __init__(self, imobject):
        self.imobject = imobject

class IFadeIn(IAnimation):
    pass

class ITransform(IAnimation):
    pass

class ICreate(IAnimation):
    pass
