import RPi.GPIO as GPIO
 
import time

GPIO.setmode(GPIO.BCM)
 
GPIO.setup(17,GPIO.IN)
 
while True:
 
  if GPIO.input(17):
     print("no rain")
  else:
     print("rain")
    
  time.sleep(1)
