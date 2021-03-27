#!/usr/bin/python
#import
import RPi.GPIO as GPIO
import time
 
# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E  = 24
LCD_D4 = 25
LCD_D5 = 12
LCD_D6 = 16
LCD_D7 = 20
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LED_CMD_NEWCHAR = 0x40 # LCD RAM address CGRAM (customer defined character)

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 
  # Initialise display
  lcd_init()
  
  newCharacter = [0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e,
                  0x04, 0x08, 0x0a, 0x12, 0x11, 0x11, 0x0a, 0x04,
                  0x04, 0x0A, 0x0a, 0x0a, 0x0a, 0x0a, 0x11, 0x00,
                  0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e,
                  0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e,
                  0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e,
                  0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e,
                  0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e]
  createNewCharacter(newCharacter)

  while True:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_byte(0x00, LCD_CHR)
    time.sleep(3)

    # Send some test
    displayChar(LCD_LINE_1, [0x00], convertToHEXForChar("! Rasbperry Pi"))
    displayChar(LCD_LINE_2, [0x01],convertToHEXForChar(" 16x2 LCD Test"))
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    displayChar(LCD_LINE_1, [0x02], convertToHEXForChar(" 1234567890123456"))
    displayChar(LCD_LINE_2, convertToHEXForChar("abcdefghijklmnop"))
 
    time.sleep(3) # 3 second delay

def convertToHEXForChar(charList):
    convertedCharList = []
    for message in charList:
      convertedCharList.append(ord(message))
    return convertedCharList
  
def displayChar(line, *args):
  concatedList = []
  for argItem in args:
    concatedList.extend(argItem)

  lcd_byte(line, LCD_CMD)
  i = 0
  for message in concatedList:
    if(i >= 16):
      break
    lcd_byte(message, LCD_CHR)
  
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def createNewCharacter(bitsList):
  # define start address for new character
  lcd_byte(LED_CMD_NEWCHAR, LCD_CMD)
  for bits in bitsList:
    lcd_byte(bits, LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()