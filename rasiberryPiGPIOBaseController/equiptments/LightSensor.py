import time
import smbus

class GY30:
  def __init__(self, address=0x23):
    bus = smbus.SMBus(1)
    self.address = address
    self.bus = bus
  
  def getLightData(self):
    if (self.bus is not None):
      data = self.bus.read_i2c_block_data(self.address, 0x11)
      return (data[1] + (256 * data[0])) / 1.2
    else:
      return 0