from collections import defaultdict
from bidict import bidict

copies = bidict()

def getCopy(imobject):
    if imobject not in copies:
        mcopy = imobject.mobject.copy()
        setCopy(imobject, mcopy)
    
    return copies[imobject]

    
def removeCopy(*mcopies):
    for mcopy in mcopies:
        original = copies.inverse[mcopy]
        del copies[original]

def setCopy(mobject, mcopy):
    copies[mobject] = mcopy 

def getOriginal(mcopy):
    return copies.inverse[mcopy] if mcopy in copies.inverse else None
