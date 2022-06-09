class IAnimation:
    """
    Intermediate animation class
    """

    def __init__(self, imobject):
        self.imobject = imobject


class IFadeIn(IAnimation):
    """
    Intermediate FadeIn class
    """


class ITransform(IAnimation):
    """
    Intermediate animation class
    """


class IReplacementTransform(IAnimation):
    """
    Intermediate replacement transform class
    """

    def __init__(self, imobject, itarget):
        super().__init__(imobject)
        self.itarget = itarget


class ICreate(IAnimation):
    """
    Intermediate animation class
    """


class IApplyFunction(IAnimation):
    """
    Intermediate animation class
    """

    def __init__(self, imobject):
        super().__init__(imobject)
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
