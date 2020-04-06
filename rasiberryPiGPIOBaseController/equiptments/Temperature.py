# Please install adafruit package firstly
# step 1 install build tools
#        sudo apt-get install build-essential python-dev
# step 2 clone project
#        git clone https://github.com/adafruit/Adafruit_Python_DHT.git
# step 3 install package
#        cd Adafruit_Python_DHT
#        sudo python3 setup.py install
#        sudo python setup.py install

import Adafruit_DHT as dht

class DHT22:
  def __init__(self, pinObj):
    self.pinObj = pinObj
    self.name = 'DHT22'
  
  def getData(self):
    sensor = dht.DHT22
    pin = self.pinObj.getPin()
    humidity, temperature = dht.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
      return round(temperature, 2), round(humidity, 2)#返回结果,精确2位
    else:
      return 0, 0