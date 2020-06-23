from rasiberryPiGPIOBaseController.equiptments.Car import CarAutoSonar
from rasiberryPiGPIOBaseController.equiptments.Car import CarMoveController
from rasiberryPiGPIOBaseController.equiptments.SimpleEquipt import Motor
from rasiberryPiGPIOBaseController.equiptments.Distance import SRF05
from rasiberryPiGPIOBaseController.RasiberryPiGPIO import RasiberryPiGPIO

board = RasiberryPiGPIO('3B+', 'BCM')
#left
leftA = board.getPin(17)
leftB = board.getPin(27)

#right
rightA = board.getPin(5)
rightB = board.getPin(6)

#sonar
trig = board.getPin(13)
echo = board.getPin(19)

leftMotor = Motor(leftA, leftB)
rightMotor = Motor(rightA, rightB)
sonar = SRF05(trig, echo)

carMotionController = CarMoveController(leftMotor, rightMotor. 6/5)

autoCar = CarAutoSonar(carMotionController, sonar)
autoCar.startMove()