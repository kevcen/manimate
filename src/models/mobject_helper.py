from collections import defaultdict
from bidict import bidict

class MobjectHandler:
    def __init__(self):
        self.copies = bidict()

    def getCopy(self, mobject):
        if mobject not in self.copies:
            mcopy = mobject.copy()
            self.setCopy(mobject, mcopy)
        
        return self.copies[mobject]
    
        
    def removeCopy(self, *mcopies):
        for mcopy in mcopies:
            original = self.copies.inverse[mcopy]
            del self.copies[original]

    def setCopy(self, mobject, mcopy):
        self.copies[mobject] = mcopy 

    def getOriginal(self, mcopy):
        return self.copies.inverse[mcopy]
