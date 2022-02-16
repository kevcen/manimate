from manim import *

class Reverser:
    def __init__(self):
        self.originals = {}
        self.copies = {}

    def reverse(self, animation):
        match animation:
            case FadeIn(mobject=mobj):
                mcopy = self.getCopy(mobj)
                self.removeCopy(mcopy)
                return FadeOut(mcopy)
            case ReplacementTransform(mobject=mobj, target_mobject=tobj):
                mcopy = self.getCopy(mobj)
                tcopy = self.getCopy(tobj)
                self.removeCopy(tcopy, mcopy)
                mcopy_ = self.getCopy(mobj)
                self.matchPosition(mcopy_, tcopy)
                return ReplacementTransform(tcopy, mcopy_)
            case Create(mobject=mobj):
                mcopy = self.getCopy(mobj)
                self.removeCopy(mcopy)
                return Uncreate(mcopy)

    def forward(self, animation):
        match animation:
            case ReplacementTransform(mobject=obj, target_mobject=tobj):
                mcopy = self.getCopy(obj)
                tcopy = self.getCopy(tobj)
                
                self.matchPosition(tcopy, mcopy)
                return ReplacementTransform(mcopy, tcopy)
            case FadeIn(mobject=obj):
                mcopy = self.getCopy(obj)
                return FadeIn(mcopy)
            case Create(mobject=obj):
                mcopy = self.getCopy(obj)
                return Create(mcopy)
        
    def matchPosition(self, mobject, target_mobject):
        mobject.match_x(target_mobject)
        mobject.match_y(target_mobject)

    def getCopy(self, mobject):
        if mobject not in self.copies:
            mcopy = mobject.copy()
            self.originals[mcopy] = mobject 
            self.copies[mobject] = mcopy 
        
   
        return self.copies[mobject]
        
    def removeCopy(self, *mcopies):
        for mcopy in mcopies:
            original = self.originals[mcopy]
            # yield original
            del self.originals[mcopy]
            del self.copies[original]


            