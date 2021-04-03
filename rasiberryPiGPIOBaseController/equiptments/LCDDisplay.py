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
    newCharacter3 = [0x00, 0x11, 0x1f, 0x15, 0x04, 0x04, 0x0e, 0x0e]
    newCharacter4 = [0x0e, 0x11, 0x15, 0x0e, 0x0e, 0x0e, 0x0e, 0x04]
    newCharacter5 = [0x03, 0x03, 0x0c, 0x10, 0x10, 0x10, 0x10, 0x0c]
    allCharacters = {
      "temperature": newCharacter1,
      "humidity": newCharacter2,
      "wind": newCharacter3,
      "light": newCharacter4,
      "degree": newCharacter5
    }
    self._device.createNewCharacterInOnce(allCharacters)
    self.displayCharForLine1([self._device.getNewCharacter('temperature')], self._device.convertToHEXForChar(" 0"), [self._device.getNewCharacter('degree')], self._device.convertToHEXForChar("    "),
                              [self._device.getNewCharacter('humidity')], self._device.convertToHEXForChar(" 0%"))
    self.displayCharForLine2([self._device.getNewCharacter('light')], self._device.convertToHEXForChar(" 0     "),
                              [self._device.getNewCharacter('wind')], self._device.convertToHEXForChar(" 0rpm"))
  
  def displayWeather(self, temperature, humidity, light, wind):
    self.displayCharFromPositionForLine1(2, 6, self._device.convertToHEXForChar(str(temperature)), [self._device.getNewCharacter('degree')])
    self.displayCharFromPositionForLine1(10, 6, self._device.convertToHEXForChar(str(humidity) + '%'))
    self.displayCharFromPositionForLine2(2, 6, self._device.convertToHEXForChar(str(light)))
    self.displayCharFromPositionForLine2(10, 6, self._device.convertToHEXForChar(str(wind) + 'rpm'))

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
  
  def displayCharFromPositionForLine1(self, position, length, *args):
    finalCharList = []
    for item in args:
      finalCharList.extend(item)
    for i in range(0, length - len(finalCharList)):
      finalCharList.extend(self._device.convertToHEXForChar(' '))
    self._device.displayCharFromPosition(LCD1602.LCD_LINE_1, position, finalCharList)
  
  def displayCharFromPositionForLine2(self, position, length, *args):
    finalCharList = []
    for item in args:
      finalCharList.extend(item)
    for i in range(0, length - len(finalCharList)):
      finalCharList.extend(self._device.convertToHEXForChar(' '))
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
  light = round(gy.getLightData())
  dhtData = dht.getData()
  temperature = dhtData[0]
  humidity = dhtData[1]
  windSpeed = round(wind.getAvgData(5))
  weatherDisplay.displayWeather(temperature, humidity, light, windSpeed)
  time.sleep(5)