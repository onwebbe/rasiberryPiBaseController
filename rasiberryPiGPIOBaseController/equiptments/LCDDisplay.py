import rasiberryPiGPIOBaseController.driver.LCD1602 as LCD1602
import sys
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin
import rasiberryPiGPIOBaseController.driver.BMP180 as BMP180
import rasiberryPiGPIOBaseController.equiptments.LightSensor as LightSensor
import rasiberryPiGPIOBaseController.equiptments.Temperature as Temperature
import rasiberryPiGPIOBaseController.equiptments.SimpleEquipt as SimpleEquipt
import time

class LCD1602WeatherDisplay:
  def __init__(self, rsPin, enablePin, D4Pin, D5Pin, D6Pin, D7Pin):
    self._device = LCD1602.LCD1602(rsPin, enablePin, D4Pin, D5Pin, D6Pin, D7Pin)
    newCharacter1 = [0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e]
    newCharacter2 = [0x04, 0x08, 0x0a, 0x12, 0x11, 0x11, 0x0a, 0x04]
    allCharacters = {
      "temperature": newCharacter1,
      "humidity": newCharacter2
    }
    self._device.createNewCharacterInOnce(allCharacters)
    self.displayCharForLine1([self._device.getNewCharacter('temperature')], self._device.convertToHEXForChar(" 0C    "),
                              [self._device.getNewCharacter('humidity')], self._device.convertToHEXForChar(" 0%    "))
    self.displayCharForLine2([self._device.getNewCharacter('temperature')], self._device.convertToHEXForChar(" 0l    "),
                              [self._device.getNewCharacter('humidity')], self._device.convertToHEXForChar(" 0rpm  "))
  
  def displayWeather(self, temperature, humidity, light, wind):
    self.displayCharFromPositionForLine1(3, self._device.convertToHEXForChar(str(temperature) + 'C'))
    self.displayCharFromPositionForLine1(11, self._device.convertToHEXForChar(str(humidity) + '%'))
    self.displayCharFromPositionForLine2(3, self._device.convertToHEXForChar(str(light) + 'l'))
    self.displayCharFromPositionForLine2(11, self._device.convertToHEXForChar(str(wind) + 'rpm'))

  def displayCharForLine1(self, *args):
    finalCharList = []
    for item in args:
      finalCharList.extend(item)
    self._device.displayChar(LCD1602.LCD_LINE_1, finalCharList)

  def displayCharForLine2(self, *args):
    finalCharList = []
    for item in args:
      finalCharList.extend(item)
    self._device.displayChar(LCD1602.LCD_LINE_2, finalCharList)
  
  def displayCharFromPositionForLine1(self, position, *args):
    finalCharList = []
    for item in args:
      finalCharList.extend(item)
    self._device.displayCharFromPosition(LCD1602.LCD_LINE_1, position, finalCharList)
  
  def displayCharFromPositionForLine2(self, position, *args):
    finalCharList = []
    for item in args:
      finalCharList.extend(item)
    self._device.displayCharFromPosition(LCD1602.LCD_LINE_2, position, finalCharList)

# isInit = False
# if len(sys.argv) == 1:
#   if sys.argv[0] == "true":
#     isInit = True

pi = RasiberryPiGPIO.RasiberryPiGPIO('3B+', 'BCM')
rsPin = pi.getPin(23)
ePin = pi.getPin(24)

D4Pin = pi.getPin(25)
D5Pin = pi.getPin(12)
D6Pin = pi.getPin(16)
D7Pin = pi.getPin(20)

bmp = BMP180.BMP180()


gy = LightSensor.GY30()


dht22Pin = pi.getPin(27)
dht = Temperature.DHT22(dht22Pin)

windPin = pi.getPin(17)

wind = SimpleEquipt.HSensorRotationV2.getInstance(windPin)
weatherDisplay = LCD1602WeatherDisplay(rsPin, ePin, D4Pin, D5Pin, D6Pin, D7Pin)

while True:
  pressure = bmp.read_pressure()
  light = round(gy.getLightData() * 10) / 10
  dhtData = dht.getData()
  temperature = dhtData[0]
  humidity = dhtData[1]
  windSpeed = round(wind.getAvgData(5))
  weatherDisplay.displayWeather(temperature, humidity, light, windSpeed)
  time.sleep(10)