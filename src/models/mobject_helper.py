from collections import defaultdict
from bidict import bidict

copies = bidict()
names = bidict()
classCtr = defaultdict(int)

def getCopy(imobject):
    if imobject not in copies:
        print('new copy')
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

def getName(imobject):
    if imobject not in names:
        cnt = classCtr[imobject.__class__]
        setName(imobject, imobject.__class__.__name__ + str(cnt))
        classCtr[imobject.__class__] += 1
    
    return names[imobject]

def setName(imobject, name):
    if name in names.inverse:
        return False #already in use 
    
    names[imobject] = name
    return True

def getImobjectByName(name):
    if name not in names.inverse:
        return None 

    return names.inverse[name]

def getImobjectsByClass(cls):
    for imobj in copies:
        if isinstance(imobj, cls):
            yield imobj 
    

