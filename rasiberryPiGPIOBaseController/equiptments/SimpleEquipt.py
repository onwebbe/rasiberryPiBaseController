import rasiberryPiGPIOBaseController.Pin as Pin
import time

class LED:
  def __init__(self, pinObj):
    self.name = 'LED'
    self.pinObj = pinObj

  def light(self):
    print('LED:', Pin.PIN_HIGH)
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
