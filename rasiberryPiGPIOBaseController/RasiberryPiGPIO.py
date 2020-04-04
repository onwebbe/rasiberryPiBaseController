# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import rasiberryPiGPIOBaseController.Pin as Pin

GPIO_TYPE_BCM = 'BCM'
GPIO_TYPE_BOARD = 'BOARD'

class RasiberryPiGPIO:
  def __init__(self, pitype, mode): # mode GPIO.BCM or GPIO.BOARD
    if (mode == GPIO_TYPE_BCM):
      GPIO.setmode(GPIO.BCM)
    else:
      GPIO.setmode(GPIO.BOARD)
    self.mode = mode
    self.type = pitype
    self.pins = []
    self._getPinByPIType()
  
  def getPin(self, number):
    pinID = None
    for pin in self.pins:
      if (self.mode == GPIO_TYPE_BCM):
        pinID = pin.getBCM()
      else:
        pinID = pin.getBOARD()
      
      if (pinID == number):
        return pin
    return Pin.Pin(-1, '', -1, -1) # return an un functionable pin object to prevent None exception

  def _getPinByPIType(self):
    type = self.type
    if (type == '3B+'):
      self.pins.append(Pin.Pin(1, self.mode, '3.3V', -1, 1))
      self.pins.append(Pin.Pin(2, self.mode, 'SDA.1', 2, 3))
      self.pins.append(Pin.Pin(3, self.mode, 'SCL.1', 3, 5))
      self.pins.append(Pin.Pin(4, self.mode, 'GPIO.7', 4, 7))
      self.pins.append(Pin.Pin(5, self.mode, 'GND', -1, 9))
      self.pins.append(Pin.Pin(6, self.mode, 'GPIO.0', 17, 11))
      self.pins.append(Pin.Pin(7, self.mode, 'GPIO.2', 27, 13))
      self.pins.append(Pin.Pin(8, self.mode, 'GPIO.3', 22, 15))
      self.pins.append(Pin.Pin(9, self.mode, '3.3C', -1, 17))
      self.pins.append(Pin.Pin(10, self.mode, 'MOSI', 10, 19))
      self.pins.append(Pin.Pin(11, self.mode, 'MISO', 9, 21))
      self.pins.append(Pin.Pin(12, self.mode, 'SCLK', 11, 23))
      self.pins.append(Pin.Pin(13, self.mode, 'GND', 0, 25))
      self.pins.append(Pin.Pin(14, self.mode, 'SDA.0', 0, 27))
      self.pins.append(Pin.Pin(15, self.mode, 'GPIO.21', 5, 29))
      self.pins.append(Pin.Pin(16, self.mode, 'GPIO.22', 6, 31))
      self.pins.append(Pin.Pin(17, self.mode, 'GPIO.23', 13, 33))
      self.pins.append(Pin.Pin(18, self.mode, 'GPIO.24', 19, 35))
      self.pins.append(Pin.Pin(19, self.mode, 'GPIO.25', 26, 37))
      self.pins.append(Pin.Pin(20, self.mode, 'GND', -1, 39))

      self.pins.append(Pin.Pin(21, self.mode, '5V', -1, 2))
      self.pins.append(Pin.Pin(22, self.mode, '5V', -1, 4))
      self.pins.append(Pin.Pin(23, self.mode, 'GND', -1, 6))
      self.pins.append(Pin.Pin(24, self.mode, 'TXD', 14, 8))
      self.pins.append(Pin.Pin(25, self.mode, 'RXD', 15, 10))
      self.pins.append(Pin.Pin(26, self.mode, 'GPIO.1', 18, 12))
      self.pins.append(Pin.Pin(27, self.mode, 'GND', -1, 14))
      self.pins.append(Pin.Pin(28, self.mode, 'GPIO.4', 23, 16))
      self.pins.append(Pin.Pin(29, self.mode, 'GPIO.5', 24, 18))
      self.pins.append(Pin.Pin(30, self.mode, 'GND', -1, 20))
      self.pins.append(Pin.Pin(31, self.mode, 'GPIO.6', 25, 22))
      self.pins.append(Pin.Pin(32, self.mode, 'CE0', 8, 24))
      self.pins.append(Pin.Pin(33, self.mode, 'CE1', 7, 26))
      self.pins.append(Pin.Pin(34, self.mode, 'SCL.0', 1, 28))
      self.pins.append(Pin.Pin(35, self.mode, 'GND', -1, 30))
      self.pins.append(Pin.Pin(36, self.mode, 'GPIO.26', 12, 32))
      self.pins.append(Pin.Pin(37, self.mode, 'GND', -1, 34))
      self.pins.append(Pin.Pin(38, self.mode, 'GPIO.27', 16, 36))
      self.pins.append(Pin.Pin(39, self.mode, 'GPIO.28', 20, 38))
      self.pins.append(Pin.Pin(40, self.mode, 'GPIO.29', 21, 40))
