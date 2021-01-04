import time
import rasiberryPiGPIOBaseController.equiptments.SimpleEquipt as SimpleEquipt
import rasiberryPiGPIOBaseController.RasiberryPiGPIO as RasiberryPiGPIO
import rasiberryPiGPIOBaseController.Pin as Pin
import time
pi = RasiberryPiGPIO.RasiberryPiGPIO('3B+', 'BCM')
pin15 = pi.getPinByBoardId(15)
pin15.setupInput()


sensor = SimpleEquipt.HSensorRotationV2.getInstance(pin15)
time.sleep(10)
print(sensor.getAvgData(3))
print(sensor._sensorDataList)
