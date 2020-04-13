import RPi.GPIO as GPIO
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
PIN_IN = "IN"
PIN_OUT = "OUT"
PIN_LOW = "LOW"
PIN_HIGH = "HIGH"

PIN_MAPPING = {
  PIN_IN: GPIO.IN,
  PIN_OUT: GPIO.OUT,
  PIN_LOW: GPIO.LOW,
  PIN_HIGH: GPIO.HIGH
}
class Pin:
  def __init__(self, pinNum, type, name, bcm, board):
    self.name = name
    self.pinNum = int(pinNum)
    if (type == RasiberryPiGPIO.GPIO_TYPE_BCM):
      self.pin = bcm
    else:
      self.pin = board
    self.frequency = 50 #标定频率为50HZ
    self.dc = 0
    self.bcm = int(bcm)
    self.board = int(board)
    #if (self.pinNum > 0):
      # GPIO.setup(self.pin, GPIO.IN)
      # GPIO.setup(pinNum, GPIO.OUT, initial=GPIO.LOW)
    
  def output_setup(self, hilow):
    if (self.pinNum > 0):
      GPIO.setup(self.pin, GPIO.OUT)
      GPIO.output(self.pin, PIN_MAPPING[hilow])
  
  def read(self):
    if (self.pinNum > 0):
      GPIO.setup(self.pin, GPIO.IN)
      return GPIO.input(self.pin)
    else:
      return -1

  def PWM_setup(self, frequency = 50):
    self.frequency = frequency
    if (self.pinNum > 0):
      GPIO.setup(self.pin, GPIO.OUT) # PWM supporting output only
      self.pwm = GPIO.PWM(self.pin, frequency)
      self.pwm.start(0)
  
  def PWM_ChangeFrequency(self, frequency):
    self.frequency = frequency
    if (self.pinNum > 0):
      self.pwm.ChangeFrequency(frequency)
  
  def PWM_ChangeDutyCycle(self, dc):
    self.dc = dc
    if (self.pinNum > 0):
      self.pwm.ChangeDutyCycle(dc)
  
  def PWM_stop(self):
    if (self.pinNum > 0):
      if (self.pwm is not None):
        self.pwm.stop()
  
  def getPin(self):
    return self.pin

  def getBCM(self):
    return self.bcm

  def getBOARD(self):
    return self.board
  
  def getName(self):
    return self.name