import rasiberryPiGPIOBaseController.Pin as Pin
import time
import _thread

class LED:
  def __init__(self, pinObj):
    self.name = 'LED'
    self.pinObj = pinObj

  def light(self):
    self.pinObj.output_setup(Pin.PIN_HIGH)

  def shutdown(self):
    self.pinObj.output_setup(Pin.PIN_LOW)
  
  def flash(self, time, howLong):
    if (howLong == 0):
      while (True):
        self.light()
        time.sleep(time)
        self.shutdown()
    else:
      count = int(howLong / time)
      for i in range(count):
        self.light()
        time.sleep(time)
        self.shutdown()

class Wheel:
  def __init__(self, pinObj):
    self.pinObj = pinObj
    self.pinObj.PWM_setup(50)
    self.name = 'Wheel'
  
  def rotate(self, angler):
    fm = 10.0/180.0
    angler = angler * fm + 2.5
    angler = int(angler * 10) / 10.0
    self.pinObj.PWM_ChangeDutyCycle(angler)

  def stop(self):
    self.pinObj.PWM_stop()

class RainDrop:
  def __init__(self, pinObj):
    self.pinObj = pinObj
    self.name = 'RainDrop'
  
  def isDrop(self):
    if self.pinObj.read():
      return False # if have data means no rain
    else:
      return True  # if no data means there is rain

class FullColorLED:
  def __init__(self, pinR, pinG, pinB):
    self.pinR = pinR
    self.pinG = pinG
    self.pinB = pinB

    self.pinR.PWM_setup(70)
    self.pinG.PWM_setup(70)
    self.pinB.PWM_setup(70)
    self.name = 'FullColorLED'
  
  def light(self, r, g, b):
    r = 100 / 255 * r
    g = 100 / 255 * g
    b = 100 / 255 * b
    self.pinR.PWM_ChangeDutyCycle(r)
    self.pinG.PWM_ChangeDutyCycle(g)
    self.pinB.PWM_ChangeDutyCycle(b)

  def stop(self):
    self.pinR.PWM_stop()
    self.pinG.PWM_stop()
    self.pinB.PWM_stop()

_HSensorRotationObject = None
class HSensorRotation:
  def __init__(self, pinObj):
    self._pinObj = pinObj
    self._name = "HSensor"
    self._counter = 0
    self._countResult = []
    self._stopIndicator = True
    self._stopCount = True
  
  @classmethod
  def getInstance(cls, pinObj):
    global _HSensorRotationObject
    if (_HSensorRotationObject is None):
       _HSensorRotationObject = HSensorRotation(pinObj)
    return _HSensorRotationObject
  
  @classmethod
  def getNewInstance(cls, pinObj):
    global _HSensorRotationObject
    _HSensorRotationObject = HSensorRotation(pinObj)
    return _HSensorRotationObject
  
  def getStatus(self):
    return self._pinObj.read(Pin.PIN_PULL_UP)
  
  def addChangeListener(self, command):
    self._pinObj.addChangeListener(Pin.PIN_PULL_RAISING, command)
  
  def _addCount(self, channel):
    if (not self._stopCount):
      self._counter = self._counter + 1

  def _startCount(self):
    self._stopIndicator = False
    self._stopCount = False
    while(not self._stopIndicator):
      self._counter = 0
      time.sleep(60)
      self._countResult.append(self._counter)
      if (len(self._countResult) > 120):
        self._countResult.remove(0)
    self._stopIndicator = True
    self._stopCount = True

  def startCount(self):
    self.addChangeListener(self._addCount)
    _thread.start_new_thread(self._startCount, ())

  def stopCount(self):
    self._stopIndicator = True
  
  def getLastCountResult(self):
    if (self._stopIndicator == True):
      self.startCount()
    if (len(self._countResult) == 0):
      return -1
    return self._countResult[len(self._countResult) - 1]
  
  def getAllCountResult(self):
    if (self._stopIndicator == True):
      self.startCount()
    return self._countResult
  
  def clearCountResult(self):
    self._countResult = []

class Motor:
  SPEED_STEP = 10
  FREQUENCY = 500
  def __init__(self, pinObj1, pinObj2):
    self._pinObj1 = pinObj1
    self._pinObj2 = pinObj2
    self._speed = 50
    self._pwm = None
    self._direction = 0
    self._pinObj1.PWM_setup(Motor.FREQUENCY)
    self._pinObj2.PWM_setup(Motor.FREQUENCY)
  
  # speed 1 - 100    direction: 0 - back >=1 - forward
  def setSpeed(self, speed):
    if (speed == 0):
      self._pinObj2.PWM_stop()
      self._pinObj1.PWM_stop()
      return
    if (speed > 100):
      speed = 100
    if (speed <= 1):
      speed = 1
    self._speed = speed
    if(self._direction):
      self._pinObj2.PWM_start(0)
      self._pinObj1.PWM_start(speed)
    else:
      self._pinObj1.PWM_start(0)
      self._pinObj2.PWM_start(speed)
  
  def stop(self):
    self._pinObj1.PWM_stop()
    self._pinObj2.PWM_stop()

  def setDirection(self, direction):
    self._direction = direction
  
  def start(self, direction = 1, speed = 50):
    self.setSpeed(speed)
  
  def speedUp(self):
    self.setSpeed(self._speed + Motor.SPEED_STEP)

  def speedDown(self):
    self.setSpeed(self._speed - Motor.SPEED_STEP)
