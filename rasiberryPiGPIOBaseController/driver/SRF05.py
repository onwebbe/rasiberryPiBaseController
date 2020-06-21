import time
import RPi.GPIO as GPIO
import _thread
import rasiberryPiGPIOBaseController.Pin as Pin
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO

class SRF05:
  def __init__(self, trigPinObj, echoPinObj):
    self._trigPinObj = trigPinObj
    self._echoPinObj = echoPinObj
    self._trigPinObj.setupOutput()
    self._echoPinObj.setupInput()
    self._startTime = 0
    self._endTime = 0
    self._startTriger = 0
  
  def _getEchoHIGH(self):
    if (self._startTriger == 1):
      self._endTime = time.time()
      self._startTriger = 0
      print(str(self._calculateDistance()))
  
  def _calculateDistance(self):
    distanceTime = self._endTime - self._startTime
    distance = 34000 * distanceTime
    return distance

  def startCheckDistance(self):
    self._checkEchoProcessor = None
    self._echoPinObj.addChangeListener(Pin.PIN_HIGH, self._getEchoHIGH)
    self._startTriger = 1
    self._startTime = time.time()

pi = RasiberryPiGPIO.RasiberryPiGPIO("3B+", "BCM")
trigPin = pi.getPin(17)
echoPin = pi.getPin(27)

srf05 = SRF05(trigPin, echoPin)
srf05.startCheckDistance()