# fopen = open('/myProject/python/rasiberryPiWebManager/gpioAPI/sampleGOIP.txt','r')
# lines = fopen.readlines()
import json
from . import GOIPStatus


def processHeadData(linedata):
    i = 0
    start = False
    startIdx = 0
    endIdx = 0
    headTitle = ''
    headList = []
    column = 0
    for letter in linedata:
        if (letter == '|'):
            if (start == True):
                endIdx = i
                headTitle = headTitle.replace('|', '')
                headTitle = headTitle.strip()
                if (headTitle == 'Physical'):
                    length = (endIdx - startIdx - 2) / 2
                    headerObj = GOIPStatus.GOIPDataHeader(linedata, headTitle, startIdx + 1, startIdx + 1 + length, column)
                    headList.append(headerObj)
                    column = 1
                    headerObj = GOIPStatus.GOIPDataHeader(linedata, headTitle, startIdx + 1 + length + 2, endIdx, column)
                    headList.append(headerObj)
                else:
                    headerObj = GOIPStatus.GOIPDataHeader(linedata, headTitle, startIdx + 1, endIdx, column)
                    headList.append(headerObj)
                endIdx = i
                startIdx = i
                headTitle = ''
            else:
                startIdx = i
                start = True
        if (start == True):
            headTitle = headTitle + letter
        i = i + 1
    return headList

def processData(linedata, headerList):
    dataList = []
    columnIDMap = {}
    for header in headerList:
        startIdx = header.start
        endIdx = header.end
        value = linedata[startIdx : endIdx]
        value = value.replace('|', '')
        value = value.strip()
        # print(header)
        gpioData = GOIPStatus.GOIPData(header, value)
        dataList.append(gpioData)
        #using Physical as id field
        if (header.title == 'Physical'):
            columnIDMap[header.col] = value
        
    # setup id
    for data in dataList:
        id = columnIDMap[data.getHeaderObj().getCol()]
        data.id = id

    return dataList

def getGPIOPinOverall(dataList):
    pinOverall = {} # key is id, value is the GPIOData object list
    for data in dataList:
        id = data.id
        if (not pinOverall.__contains__(id)):
            pinOverall[id] = []
        pinOverall[id].append(data)
    return pinOverall

def createGPIOOverallObject(pinOverall):
    pinList = []
    for pinid in pinOverall:
        pinNames = {}
        pinValue = ''
        pinMode = ''
        pinDataList = pinOverall[pinid]
        for pinDataItem in pinDataList:
            pinTitle = pinDataItem.getTitle()
            if (pinTitle == 'V'):
                pinValue = pinDataItem.value
            elif (pinTitle == 'Mode'):
                pinMode = pinDataItem.value
            else:
                pinNames[pinTitle] = pinDataItem.value
        pinObj = GOIPStatus.GPIOPin(int(pinDataItem.id), pinMode, pinValue, pinNames)
        pinList.append(pinObj)
    return pinList

def parseGOIPStatusData(inputString):
    # if (lineArray == None):
    #     lineArray = lines
    i = 0
    headList = None
    dataList = []
    headerIndCount = 0
    lineArray = inputString.splitlines()
    for line in lineArray:
        if (i == 1):
            headList = processHeadData(line)
        elif (line.find('+---') > 0):
            headerIndCount = headerIndCount + 1
            if (headerIndCount > 2):
                break
        elif (headList != None):
            tmpList = processData(line, headList)
            for tmpHeader in tmpList:
                dataList.append(tmpHeader)
        i = i + 1
    
    # return dataList
    pinOverallMap = getGPIOPinOverall(dataList)
    pinOverallObj = createGPIOOverallObject(pinOverallMap)
    return pinOverallObj

# displayDataList = parseGOIPStatusData(None)
# for data in displayDataList:
#     print(data)