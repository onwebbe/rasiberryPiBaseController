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
  def __init__(self, type, pinNum, name, bcm, board):
    self.name = name
    self.pinNum = pinNum
    if (type == RasiberryPiGPIO.GPIO_TYPE_BCM):
      self.pin = bcm
    else:
      self.pin = board
    self.frequency = 50 #标定频率为50HZ
    self.dc = 0
    self.bcm = bcm
    self.board = board
    if (self.pin > 0):
      GPIO.setup(pinNum, GPIO.IN)
      # GPIO.setup(pinNum, GPIO.OUT, initial=GPIO.LOW)
    
  def output_setup(self, hilow):
    if (self.pin > 0):
      GPIO.setup(self.pin, GPIO.OUT)
      GPIO.output(self.pin, PIN_MAPPING[hilow])
  
  def read(self):
    if (self.pin > 0):
      return GPIO.input(self.pin)
    else:
      return -1

  def PWM_setup(self, frequency):
    self.frequency = frequency
    if (self.pin > 0):
      self.pwm = GPIO.PWM(self.pin, frequency)
      self.pwm.start(0)
  
  def PWM_ChangeFrequency(self, frequency):
    self.frequency = frequency
    if (self.pin > 0):
      self.pwm.ChangeFrequency(frequency)
  
  def PWM_ChangeDutyCycle(self, dc):
    self.dc = dc
    if (self.pin > 0):
      self.pwm.ChangeDutyCycle(dc)
  
  def PWM_stop(self):
    if (self.pin > 0):
      if (self.pwm is not None):
        self.pwm.stop()
  
  def getBCM(self):
    return self.bcm

  def getBOARD(self):
    return self.board
  
  def getName(self):
    return self.name