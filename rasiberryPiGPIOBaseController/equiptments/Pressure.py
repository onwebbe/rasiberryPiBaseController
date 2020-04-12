import time
import rasiberryPiGPIOBaseController.driver.BMP180 as devBMP180


class BMP180:
  def __init__(self, address=0x77):
    self._address = address
    self.device = devBMP180.BMP180(address)
  
  def getTemperature(self):
    return self.device.read_temperature()
  
  def getPressure(self):
    return self.device.read_pressure()

  def getAltitude(self):
    return self.device.read_altitude()