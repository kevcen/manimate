from collections import defaultdict
from bidict import bidict

class MobjectHandler:
    def __init__(self):
        self.copies = bidict()

    def getCopy(self, imobject):
        if imobject not in self.copies:
            mcopy = imobject.mobject.copy()
            self.setCopy(imobject, mcopy)
        
        return self.copies[imobject]
    
        
    def removeCopy(self, *mcopies):
        for mcopy in mcopies:
            original = self.copies.inverse[mcopy]
            del self.copies[original]

    def setCopy(self, mobject, mcopy):
        self.copies[mobject] = mcopy 

    def getOriginal(self, mcopy):
        return self.copies.inverse[mcopy] if mcopy in self.copies.inverse else None
