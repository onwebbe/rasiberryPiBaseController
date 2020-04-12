import json
class GOIPData:
    """GOIP Data类实例"""
    id = ''
    value = ''
    __headerObj = None
    def __init__(self, headObj, value):
        self.__headerObj = headObj
        self.id = id
        self.value = value
    
    def getTitle(self):
        return self.__headerObj.title

    def getHeaderObj(self):
        return self.__headerObj

    def getJSONObj(self):
        jsonObj = {"id": self.id, "value": self.value, "headerObj": self.__headerObj.getJSONObj()}
        return jsonObj

    def __str__(self):
        return '%s - %s : %s' %(self.id, self.__headerObj.getTitle(), self.value)

class GOIPDataHeader:
    """GOIP Data类表头实例"""
    title = ''
    start = 0
    end = 0
    _rawtext = ''
    col = 0
    def __init__(self, raw, title, start, end, col):
        self.title = title
        self.start = int(start)
        self.end = int(end)
        self._rawtext = raw
        self.col = col

    def getRawHeader(self):
        # print (self.start, ':', self.end)
        return self._rawtext[self.start : self.end]
    
    def getCol(self):
        return self.col
    
    def getTitle(self):
        return self.title

    def getJSONObj(self):
        jsonObj = {"title": self.title, "start": self.start, "end": self.end, "col": self.col}
        return jsonObj

    def __str__(self):
        return 'column:%d title:%s  startIndex:%d  endIndex:%d' %(self.col, self.title, self.start, self.end)

class GPIOPin:
    __pinID = -1
    __pinValue = -1
    __pinMode = ''
    __pinNames = {}
    def __init__(self, pinID, pinMode, pinValue, pinNames):
        self.__pinValue = pinValue
        self.__pinNames = pinNames 
        self.__pinMode = pinMode
        self.__pinID = pinID

    def getPinID(self):
        return self.__pinID
        
    def getJSONObj(self):
        jsonObj = {"value": self.__pinValue, "mode": self.__pinMode, "names": self.__pinNames}
        return jsonObj
    
    def __str__(self):
        names = ''
        for name in self.__pinNames:
            names = names + ' : ' + name + '-' + self.__pinNames[name]
        return 'id:%s mode:%s value:%s names:%s' %(self.__pinID, self.__pinMode, self.__pinValue, names)