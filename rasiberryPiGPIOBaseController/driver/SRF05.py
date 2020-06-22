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
  
  def _calculateDistance(self):
    distanceTime = self._endTime - self._startTime
    distance = 34000 * distanceTime / 2
    return distance

  def _startToTriger(self):
    self._trigPinObj.output_setup(Pin.PIN_HIGH)
    # self._startTime = time.time()
    time.sleep(0.01)
    self._trigPinObj.output_setup(Pin.PIN_LOW)

  def startCheckDistance(self):
    self._checkEchoProcessor = None
    self._startTriger = 1
    _thread.start_new_thread(self._startToTriger, ())
    while(not self._echoPinObj.read() == GPIO.HIGH):
      pass
    self._startTime = time.time()
    
    while(not self._echoPinObj.read() == GPIO.LOW):
      pass
    self._endTime = time.time()
    return self._calculateDistance()
