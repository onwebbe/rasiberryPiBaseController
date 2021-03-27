import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin
import rasiberryPiGPIOBaseController.driver.LCD1602 as LCD1602
import time
pi = RasiberryPiGPIO.RasiberryPiGPIO('3B+', 'BCM')
rsPin = pi.getPin(23)
ePin = pi.getPin(24)

D4Pin = pi.getPin(25)
D5Pin = pi.getPin(1)
D6Pin = pi.getPin(12)
D7Pin = pi.getPin(16)

lcd = LCD1602.LCD1602(rsPin, ePin, D4Pin, D5Pin, D6Pin, D7Pin)
lcd.simpleDemo()