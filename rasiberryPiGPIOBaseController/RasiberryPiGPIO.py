# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import rasiberryPiGPIOBaseController.Pin as Pin
from . import processGPIOStatus
import os
GPIO_TYPE_BCM = 'BCM'
GPIO_TYPE_BOARD = 'BOARD'

sampleGPIOStr = ''' +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 | ALT0 | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 | ALT0 | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 0 |  7 || 8  | 0 | IN   | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |  OUT | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | IN   | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+'''

class RasiberryPiGPIO:
  def __init__(self, pitype, mode): # mode GPIO.BCM or GPIO.BOARD
    if (mode == GPIO_TYPE_BCM):
      GPIO.setmode(GPIO.BCM)
    else:
      GPIO.setmode(GPIO.BOARD)
    self.mode = mode
    self.type = pitype
    self.pins = []
    self._getPinByPITypeAuto()
  
  def getPinByBoardId(self, boardId):
    for pin in self.pins:
      if (pin.getBOARD() == boardId):
        return pin
    return None

  def getMode(self):
    return self.mode
  
  def getType(self):
    return self.type

  def getPin(self, number):
    pinID = None
    for pin in self.pins:
      if (self.mode == GPIO_TYPE_BCM):
        pinID = int(pin.getBCM())
      else:
        pinID = int(pin.getBOARD())
      
      if (pinID == number):
        return pin
    return Pin.Pin(-1, self.mode, '', -1, -1) # return an un functionable pin object to prevent None exception

  def _getPinByPITypeAuto(self):
    gpioStatusString = None
    if (GPIO.MOCK is not None and GPIO.MOCK == True):
      gpioStatusString = sampleGPIOStr
    else:
      output = os.popen('gpio readall')
      gpioStatusString = output.read()
    dataList = processGPIOStatus.parseGOIPStatusData(gpioStatusString)
    for pinData in dataList:
      pinJson = pinData.getJSONObj()
      pin = pinJson['names']['Physical']
      bcm = pinJson['names']['BCM']
      if (bcm is None or bcm == ''):
        bcm = -1
      name = pinJson['names']['Name']
      pinObj = Pin.Pin(pin, self.mode, name, bcm, pin)
      self.pins.append(pinObj)
    # dataList = [ { "value": "", "mode": "", "names": { "BCM": "", "wPi": "", "Name": "3.3v", "Physical": "1" } }, { "value": "", "mode": "", "names": { "Physical": "2", "Name": "5v", "wPi": "", "BCM": "" } }, { "value": "1", "mode": "IN", "names": { "BCM": "2", "wPi": "8", "Name": "SDA.1", "Physical": "3" } }, { "value": "", "mode": "", "names": { "Physical": "4", "Name": "5v", "wPi": "", "BCM": "" } }, { "value": "1", "mode": "IN", "names": { "BCM": "3", "wPi": "9", "Name": "SCL.1", "Physical": "5" } }, { "value": "", "mode": "", "names": { "Physical": "6", "Name": "0v", "wPi": "", "BCM": "" } }, { "value": "1", "mode": "IN", "names": { "BCM": "4", "wPi": "7", "Name": "GPIO. 7", "Physical": "7" } }, { "value": "0", "mode": "OUT", "names": { "Physical": "8", "Name": "TxD", "wPi": "15", "BCM": "14" } }, { "value": "", "mode": "", "names": { "BCM": "", "wPi": "", "Name": "0v", "Physical": "9" } }, { "value": "0", "mode": "OUT", "names": { "Physical": "10", "Name": "RxD", "wPi": "16", "BCM": "15" } }, { "value": "0", "mode": "IN", "names": { "BCM": "17", "wPi": "0", "Name": "GPIO. 0", "Physical": "11" } }, { "value": "0", "mode": "IN", "names": { "Physical": "12", "Name": "GPIO. 1", "wPi": "1", "BCM": "18" } }, { "value": "0", "mode": "IN", "names": { "BCM": "27", "wPi": "2", "Name": "GPIO. 2", "Physical": "13" } }, { "value": "", "mode": "", "names": { "Physical": "14", "Name": "0v", "wPi": "", "BCM": "" } }, { "value": "0", "mode": "IN", "names": { "BCM": "22", "wPi": "3", "Name": "GPIO. 3", "Physical": "15" } }, { "value": "0", "mode": "IN", "names": { "Physical": "16", "Name": "GPIO. 4", "wPi": "4", "BCM": "23" } }, { "value": "", "mode": "", "names": { "BCM": "", "wPi": "", "Name": "3.3v", "Physical": "17" } }, { "value": "0", "mode": "IN", "names": { "Physical": "18", "Name": "GPIO. 5", "wPi": "5", "BCM": "24" } }, { "value": "0", "mode": "IN", "names": { "BCM": "10", "wPi": "12", "Name": "MOSI", "Physical": "19" } }, { "value": "", "mode": "", "names": { "Physical": "20", "Name": "0v", "wPi": "", "BCM": "" } }, { "value": "0", "mode": "IN", "names": { "BCM": "9", "wPi": "13", "Name": "MISO", "Physical": "21" } }, { "value": "0", "mode": "IN", "names": { "Physical": "22", "Name": "GPIO. 6", "wPi": "6", "BCM": "25" } }, { "value": "0", "mode": "IN", "names": { "BCM": "11", "wPi": "14", "Name": "SCLK", "Physical": "23" } }, { "value": "0", "mode": "IN", "names": { "Physical": "24", "Name": "CE0", "wPi": "10", "BCM": "8" } }, { "value": "", "mode": "", "names": { "BCM": "", "wPi": "", "Name": "0v", "Physical": "25" } }, { "value": "1", "mode": "IN", "names": { "Physical": "26", "Name": "CE1", "wPi": "11", "BCM": "7" } }, { "value": "1", "mode": "IN", "names": { "BCM": "0", "wPi": "30", "Name": "SDA.0", "Physical": "27" } }, { "value": "1", "mode": "IN", "names": { "Physical": "28", "Name": "SCL.0", "wPi": "31", "BCM": "1" } }, { "value": "1", "mode": "IN", "names": { "BCM": "5", "wPi": "21", "Name": "GPIO.21", "Physical": "29" } }, { "value": "", "mode": "", "names": { "Physical": "30", "Name": "0v", "wPi": "", "BCM": "" } }, { "value": "1", "mode": "IN", "names": { "BCM": "6", "wPi": "22", "Name": "GPIO.22", "Physical": "31" } }, { "value": "0", "mode": "IN", "names": { "Physical": "32", "Name": "GPIO.26", "wPi": "26", "BCM": "12" } }, { "value": "0", "mode": "IN", "names": { "BCM": "13", "wPi": "23", "Name": "GPIO.23", "Physical": "33" } }, { "value": "", "mode": "", "names": { "Physical": "34", "Name": "0v", "wPi": "", "BCM": "" } }, { "value": "0", "mode": "IN", "names": { "BCM": "19", "wPi": "24", "Name": "GPIO.24", "Physical": "35" } }, { "value": "0", "mode": "IN", "names": { "Physical": "36", "Name": "GPIO.27", "wPi": "27", "BCM": "16" } }, { "value": "0", "mode": "IN", "names": { "BCM": "26", "wPi": "25", "Name": "GPIO.25", "Physical": "37" } }, { "value": "0", "mode": "IN", "names": { "Physical": "38", "Name": "GPIO.28", "wPi": "28", "BCM": "20" } }, { "value": "", "mode": "", "names": { "BCM": "", "wPi": "", "Name": "0v", "Physical": "39" } }, { "value": "0", "mode": "IN", "names": { "Physical": "40", "Name": "GPIO.29", "wPi": "29", "BCM": "21" } } ]
    return dataList

  def _getPinByPIType(self):
    type = self.type
    if (type == '3B+'):
      self.pins.append(Pin.Pin(1, self.mode, '3.3V', -1, 1))
      self.pins.append(Pin.Pin(2, self.mode, '5V', -1, 2))
      self.pins.append(Pin.Pin(3, self.mode, 'SDA.1', 2, 3))
      self.pins.append(Pin.Pin(4, self.mode, '5V', -1, 4))
      self.pins.append(Pin.Pin(5, self.mode, 'SCL.1', 3, 5))
      self.pins.append(Pin.Pin(6, self.mode, 'GND', -1, 6))
      self.pins.append(Pin.Pin(7, self.mode, 'GPIO.7', 4, 7))
      self.pins.append(Pin.Pin(8, self.mode, 'TXD', 14, 8))
      self.pins.append(Pin.Pin(9, self.mode, 'GND', -1, 9))
      self.pins.append(Pin.Pin(10, self.mode, 'RXD', 15, 10))
      self.pins.append(Pin.Pin(11, self.mode, 'GPIO.0', 17, 11))
      self.pins.append(Pin.Pin(12, self.mode, 'GPIO.1', 18, 12))
      self.pins.append(Pin.Pin(13, self.mode, 'GPIO.2', 27, 13))
      self.pins.append(Pin.Pin(14, self.mode, 'GND', -1, 14))
      self.pins.append(Pin.Pin(15, self.mode, 'GPIO.3', 22, 15))
      self.pins.append(Pin.Pin(16, self.mode, 'GPIO.4', 23, 16))
      self.pins.append(Pin.Pin(17, self.mode, '3.3C', -1, 17))
      self.pins.append(Pin.Pin(18, self.mode, 'GPIO.5', 24, 18))
      self.pins.append(Pin.Pin(19, self.mode, 'MOSI', 10, 19))
      self.pins.append(Pin.Pin(20, self.mode, 'GND', -1, 20))
      self.pins.append(Pin.Pin(21, self.mode, 'MISO', 9, 21))
      self.pins.append(Pin.Pin(22, self.mode, 'GPIO.6', 25, 22))
      self.pins.append(Pin.Pin(23, self.mode, 'SCLK', 11, 23))
      self.pins.append(Pin.Pin(24, self.mode, 'CE0', 8, 24))
      self.pins.append(Pin.Pin(25, self.mode, 'GND', 0, 25))
      self.pins.append(Pin.Pin(26, self.mode, 'CE1', 7, 26))
      self.pins.append(Pin.Pin(27, self.mode, 'SDA.0', 0, 27))
      self.pins.append(Pin.Pin(28, self.mode, 'SCL.0', 1, 28))
      self.pins.append(Pin.Pin(29, self.mode, 'GPIO.21', 5, 29))
      self.pins.append(Pin.Pin(30, self.mode, 'GND', -1, 30))
      self.pins.append(Pin.Pin(31, self.mode, 'GPIO.22', 6, 31))
      self.pins.append(Pin.Pin(32, self.mode, 'GPIO.26', 12, 32))
      self.pins.append(Pin.Pin(33, self.mode, 'GPIO.23', 13, 33))
      self.pins.append(Pin.Pin(34, self.mode, 'GND', -1, 34))
      self.pins.append(Pin.Pin(35, self.mode, 'GPIO.24', 19, 35))
      self.pins.append(Pin.Pin(36, self.mode, 'GPIO.27', 16, 36))
      self.pins.append(Pin.Pin(37, self.mode, 'GPIO.25', 26, 37))
      self.pins.append(Pin.Pin(38, self.mode, 'GPIO.28', 20, 38))
      self.pins.append(Pin.Pin(39, self.mode, 'GND', -1, 39))
      self.pins.append(Pin.Pin(40, self.mode, 'GPIO.29', 21, 40))

      
      
      
      
      
      
      
      
      
      
