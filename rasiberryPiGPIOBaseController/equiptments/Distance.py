from rasiberryPiGPIOBaseController.driver.SRF05 import SRF05 as SRF05Driver
import _thread
import time

class SRF05:
  def __init__(self, trigObj, echoObj):
    self._device = SRF05Driver(trigObj, echoObj)
    self._isStart = False
    self._currentDistance = 0
  
  def getOneTimeDistance(self):
    self._currentDistance = self._device.startCheckDistance()
    return self._currentDistance
  
  def _getLoopingDistance(self, gap):
    while(self._isStart):
      self.getOneTimeDistance()
      time.sleep(gap)
  
  def stopDistanceCheck(self):
    self._isStart = False

  def startDistanceCheck(self, gap = 1):
    self._isStart = True
    if (gap < 0.1):
      gap = 0.1
    _thread.start_new_thread(self._getLoopingDistance, (gap))
