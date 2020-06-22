from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import Motor
import _thread
import time

class CarAutoSonar:
  def __init__(self, movingController, sonarDevice):
    self._movingController = movingController
    self._sonarDevice = sonarDevice
    self._isStart = False
    self._movingController.noMove()
  
  def _sonarCheck(self):
    while(self._isStart):
      distance = self._sonarDevice.getOneTimeDistance()
      if (distance < 30):
        self._movingController.rotate('left')
      else:
        self._movingController.moveForward(50)
      
      time.sleep(0.3)

  def startMove(self):
    self._isStart = True
    _thread.start_new_thread(self._sonarCheck, ())
  
  def stop(self):
    self._isStart = False


class CarMoveController:
  #balanceRatio   speed of left / speed of right to make car go strictly
  def __init__(self, leftMotor, rightMotor, balanceRatio = (5/6)):
    self._leftMotor = leftMotor
    self._rightMotor = rightMotor
    self._balanceRatio = balanceRatio
    self._rightMotor.start(0)
    self._leftMotor.start(0)

  def setCarSpeed(self, speed):
    if (speed <= 50):
      speed = 50
    leftSpeed = speed
    rightSpeed = speed / self._balanceRatio
    self._leftMotor.setSpeed(leftSpeed)
    self._rightMotor.setSpeed(rightSpeed)
  
  def moveBackward(self, speed):
    self._leftMotor.setDirection(0)
    self._rightMotor.setDirection(0)
    self.setCarSpeed(speed)
  
  def moveForward(self, speed):
    self._leftMotor.setDirection(1)
    self._rightMotor.setDirection(1)
    self.setCarSpeed(speed)
  
  def rotate(self, direction, type = "normal", time = 1):
    self.noMove()
    speed = 50
    if (type == 'superfast'):
      speed = 100
    
    if (direction == 'left'):
      self._rightMotor.setDirection(1)
      self._rightMotor.setSpeed(speed / self._balanceRatio)
      if (type == 'fast'):
        self._leftMotor.setDirection(1)
        self._leftMotor.setSpeed(speed)
    time.sleep(time)
    self.noMove()

  def noMove(self):
    speed = 0
    leftSpeed = speed
    rightSpeed = speed / self._balanceRatio
    self._leftMotor.setSpeed(leftSpeed)
    self._rightMotor.setSpeed(rightSpeed)
  
  def stop(self):
    self._leftMotor.stop()
    self._rightMotor.stop()