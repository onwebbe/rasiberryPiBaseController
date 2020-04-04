import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin
import time
pi = RasiberryPiGPIO.RasiberryPiGPIO('3B+', 'BCM')
pin4 = pi.getPin(4)
pin4.output_setup(Pin.PIN_HIGH)
time.sleep(5)
pin4.output_setup(Pin.PIN_LOW)
