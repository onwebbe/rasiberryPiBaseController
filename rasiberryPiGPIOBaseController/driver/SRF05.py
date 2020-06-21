import time
import RPi.GPIO as GPIO
import _thread
import rasiberryPiGPIOBaseController.Pin as Pin
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO

class SRF05:
  def __init__(self, trigPinObj, echoPinObj):
    self._trigPinObj = trigPinObj
    self._echoPinObj = echoPinObj
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.IN)
    self._startTime = 0
    self._endTime = 0
    self._startTriger = 0
  
  def _calculateDistance(self):
    distanceTime = self._endTime - self._startTime
    distance = 34000 * distanceTime / 2
    return distance

  def _startToTriger(self):
    GPIO.output(5, GPIO.HIGH)
    # self._startTime = time.time()
    time.sleep(0.01)
    GPIO.output(5, GPIO.LOW)

  def startCheckDistance(self):
    self._checkEchoProcessor = None
    self._startTriger = 1
    _thread.start_new_thread(self._startToTriger, ())
    while(not GPIO.input(6) == GPIO.HIGH):
      pass
    self._startTime = time.time()
    
    while(not GPIO.input(6) == GPIO.LOW):
      pass
    self._endTime = time.time()
    print(self._calculateDistance())
