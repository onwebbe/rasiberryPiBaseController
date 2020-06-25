from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import Motor
import _thread
import time


class CarAutoSonar:
  ROTATION_TIME = 0.5
  SONAR_CHECK_TIME_GAP = 0.1
  CRASH_DISTANCE_LIMIT = 40
  def __init__(self, movingController, sonarDevice):
    self._movingController = movingController
    self._sonarDevice = sonarDevice
    self._isStart = False
    self._movingController.noMove()
    self._rotation_time = CarAutoSonar.ROTATION_TIME
    self._sonar_check_time_gap = CarAutoSonar.SONAR_CHECK_TIME_GAP
    self._crash_distance_limit = CarAutoSonar.CRASH_DISTANCE_LIMIT
  
  def setRotationTime(self, time):
    self._rotation_time = time
  
  def setSonarCheckTimeGap(self, time):
    self._sonar_check_time_gap = time

  def setCrashDistance(self, distance):
    self._crash_distance_limit = distance

  def _sonarCheck(self):
    while(self._isStart):
      distance = self._sonarDevice.getOneTimeDistance()
      if (distance < self._crash_distance_limit):
        self._movingController.rotate('left', 'normal', self._rotation_time)
      else:
        self._movingController.moveForward(0)
      time.sleep(self._sonar_check_time_gap)
    self._movingController.stop()

  def startMove(self):
    self._isStart = True
    _thread.start_new_thread(self._sonarCheck, ())
  
  def stop(self):
    self._isStart = False


class CarMoveController:
  #balanceRatio   speed of left / speed of right to make car go strictly
  def __init__(self, leftMotor, rightMotor, balanceRatio = (5/7)):
    self._leftMotor = leftMotor
    self._rightMotor = rightMotor
    self._balanceRatio = balanceRatio
    self._rightMotor.start(0)
    self._leftMotor.start(0)
    self._speed = 50
  
  def setBalanceRatio(self, ratio):
    self._balanceRatio = ratio
    self.setCarSpeed(self._speed)

  def setCarSpeed(self, speed):
    if (speed <= 10):
      speed = 10
    self._speed = speed
    leftSpeed = speed
    rightSpeed = speed / self._balanceRatio
    self._leftMotor.setSpeed(leftSpeed)
    self._rightMotor.setSpeed(rightSpeed)
  
  def moveBackward(self, speed):
    self._leftMotor.setDirection(0)
    self._rightMotor.setDirection(0)
    self.setCarSpeed(speed)
  
  def moveForward(self, speed):
    if (speed == 0):
      speed = self._speed
    self._leftMotor.setDirection(1)
    self._rightMotor.setDirection(1)
    self.setCarSpeed(speed)
  
  def rotate(self, direction, type = "normal", sleepTime = 1):
    self.noMove()
    speed = 50
    if (type == 'superfast'):
      speed = 100
    elif (type == 'slow'):
      speed = 10
    
    if (direction == 'left'):
      self._rightMotor.setDirection(1)
      self._rightMotor.setSpeed(speed / self._balanceRatio)
      if (type == 'fast' or type == 'superfast'):
        self._leftMotor.setDirection(1)
        self._leftMotor.setSpeed(speed)
    time.sleep(sleepTime)
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
