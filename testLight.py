import time
import smbus

bus = smbus.SMBus(1)
addr = 0x23
data = bus.read_i2c_block_data(addr,0x11)
while True:
  print ("Luminosity " + str((data[1] + (256 * data[0])) / 1.2) + "lx")
  time.sleep(1)