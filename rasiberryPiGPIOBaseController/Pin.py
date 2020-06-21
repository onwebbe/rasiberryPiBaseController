import RPi.GPIO as GPIO
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
PIN_IN = "IN"
PIN_OUT = "OUT"
PIN_LOW = "LOW"
PIN_HIGH = "HIGH"
PIN_PULL_UP = "PULL_UP"
PIN_PULL_DOWN = "PULL_DOWN"
PIN_PULL_RAISING = "PULL_RAISING"
PIN_PULL_FALLING = "PULL_FULLING"
PIN_PULL_BOTH = "PULL_BOTH"
PIN_MAPPING = {
  PIN_IN: GPIO.IN,
  PIN_OUT: GPIO.OUT,
  PIN_LOW: GPIO.LOW,
  PIN_HIGH: GPIO.HIGH
}

PIN_PULL = {
  PIN_PULL_UP: GPIO.PUD_UP,
  PIN_PULL_DOWN: GPIO.PUD_DOWN,
  PIN_PULL_RAISING: GPIO.RISING,
  PIN_PULL_FALLING: GPIO.FALLING,
  PIN_PULL_BOTH: GPIO.BOTH,
}
class Pin:
  def __init__(self, pinNum, type, name, bcm, board, in_out, value):
    self.name = name
    self.pinNum = int(pinNum)
    if (type == RasiberryPiGPIO.GPIO_TYPE_BCM):
      self.pin = int(bcm)
    else:
      self.pin = int(board)
    self.frequency = 50 #标定频率为50HZ
    self.dc = 0
    self.bcm = int(bcm)
    self.board = int(board)
    self.mode = in_out
    self.value = value
    #if (self.pinNum > 0):
      # GPIO.setup(self.pin, GPIO.IN)
      # GPIO.setup(pinNum, GPIO.OUT, initial=GPIO.LOW)
  
  def setupInput(self):
    GPIO.setup(self.pin, GPIO.IN)

  def setupOutput(self):
    GPIO.setup(self.pin, GPIO.OUT)
  
  def output_setup(self, hilow):
    if (self.pinNum > 0):
      # print (self.pin)
      # print ('BOARD:%d'%(self.board))
      # print ('BCM:%d'%(self.bcm))
      # print (self.mode)
      # print (hilow)
      GPIO.setup(self.pin, GPIO.OUT)
      GPIO.output(self.pin, PIN_MAPPING[hilow])
      self.value = PIN_MAPPING[hilow]
      self.mode = PIN_OUT
  
  def read(self, updown = None):
    if (self.pinNum > 0):
      if (updown is not None):
        GPIO.setup(self.pin, GPIO.IN, PIN_PULL[updown])
      else:
        GPIO.setup(self.pin, GPIO.IN)
      self.mode = PIN_IN
      return GPIO.input(self.pin)
    else:
      return -1

  def PWM_setup(self, frequency = 50):
    self.mode = ''
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
  
  def getMode(self):
    return self.mode

  def getValue(self):
    return self.value
  
  def addChangeListener(self, updown, command):
    GPIO.setup(self.pin, GPIO.IN)
    GPIO.add_event_detect(self.pin, PIN_PULL[updown], command)
  
  def removeChangeListener(self):
    GPIO.remove_event_detect(self.pin)