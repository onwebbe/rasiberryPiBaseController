#!/usr/bin/python
#import
import RPi.GPIO as GPIO
import time
 
# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E  = 24
LCD_D4 = 25
LCD_D5 = 1
LCD_D6 = 12
LCD_D7 = 16
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = 'PIN_HIGH'
LCD_CMD = 'PIN_LOW'
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LED_CMD_NEWCHAR = 0x40 # LCD RAM address CGRAM (customer defined character)

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

class LCD1602:
  def __init__(self, rsPin, enablePin, D4Pin, D5Pin, D6Pin, D7Pin):
    self._newCharacters = {}
    self._rsPin = rsPin
    self._enablePin = enablePin
    self._D4Pin = D4Pin
    self._D5Pin = D5Pin
    self._D6Pin = D6Pin
    self._D7Pin = D7Pin
    # initial all output pins
    self._rsPin.setupOutput()  # RS
    self._enablePin.setupOutput() # E
    self._D4Pin.setupOutput() # DB4
    self._D4Pin.setupOutput() # DB5
    self._D4Pin.setupOutput() # DB6
    self._D4Pin.setupOutput() # DB7
    self.lcd_init()

    # initial LCD functions
  def lcd_init(self):
    # Initialise display
    self.lcd_send_byte(0x33, LCD_CMD) # 110011 Initialise
    self.lcd_send_byte(0x32, LCD_CMD) # 110010 Initialise
    self.lcd_send_byte(0x06, LCD_CMD) # 000110 Cursor move direction
    self.lcd_send_byte(0x0C, LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    self.lcd_send_byte(0x28, LCD_CMD) # 101000 Data length, number of lines, font size
    self.lcd_send_byte(0x01, LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)

  def lcd_send_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = PIN_LOW for character
    #        PIN_HIGH for command
    self._rsPin.output_setup(mode) # RS
  
    # High bits
    self._D4Pin.output_setup("PIN_LOW")
    self._D5Pin.output_setup("PIN_LOW")
    self._D6Pin.output_setup("PIN_LOW")
    self._D7Pin.output_setup("PIN_LOW")

    if bits&0x10==0x10:
      self._D4Pin.output_setup("PIN_HIGH")
    if bits&0x20==0x20:
      self._D5Pin.output_setup("PIN_HIGH")
    if bits&0x40==0x40:
      self._D6Pin.output_setup("PIN_HIGH")
    if bits&0x80==0x80:
      self._D7Pin.output_setup("PIN_HIGH")
  
    # Toggle 'Enable' pin
    self.lcd_toggle_enable()
  
    # Low bits
    self._D4Pin.output_setup("PIN_LOW")
    self._D5Pin.output_setup("PIN_LOW")
    self._D6Pin.output_setup("PIN_LOW")
    self._D7Pin.output_setup("PIN_LOW")
    if bits&0x01==0x01:
      self._D4Pin.output_setup("PIN_HIGH")
    if bits&0x02==0x02:
      self._D5Pin.output_setup("PIN_HIGH")
    if bits&0x04==0x04:
      self._D6Pin.output_setup("PIN_HIGH")
    if bits&0x08==0x08:
      self._D7Pin.output_setup("PIN_HIGH")
  
    # Toggle 'Enable' pin
    self.lcd_toggle_enable()

  # toggle enable pin to accept high or low value of the data
  def lcd_toggle_enable(self):
    # Toggle enable
    time.sleep(E_DELAY)
    self._enablePin.output_setup('PIN_HIGH')
    time.sleep(E_PULSE)
    self._enablePin.output_setup('PIN_LOW')
    time.sleep(E_DELAY)

  def convertToHEXForChar(self, charList):
    convertedCharList = []
    for message in charList:
      convertedCharList.append(ord(message))
    return convertedCharList
  
  def displayChar(self, line, *args):
    concatedList = []
    for argItem in args:
      concatedList.extend(argItem)

    self.lcd_send_byte(line, LCD_CMD)
    i = 0
    for message in concatedList:
      if(i >= 16):
        break
      self.lcd_send_byte(message, LCD_CHR)
  
  def displayCharFromPosition(self, line, position, *args):
    concatedList = []
    for argItem in args:
      concatedList.extend(argItem)

    self.lcd_send_byte(line, LCD_CMD + (0x40 * position))
    i = 0
    for message in concatedList:
      if(i >= (16 - position)):
        break
      self.lcd_send_byte(message, LCD_CHR)

  def createNewCharacterInOnce(self, bitsList):
    # define start address for new character
    self.lcd_send_byte(LED_CMD_NEWCHAR, LCD_CMD)
    i = 0
    for bits in bitsList:
      self.lcd_send_byte(bits, LCD_CHR)
      self._newCharacters[str(i)] = i
      i += 1
  
  def createOneNewCharacter(self, name, position, bitsList):
    # define start address for new character
    self.lcd_send_byte(LED_CMD_NEWCHAR + (0x40 * position), LCD_CMD)
    i = 0
    for bits in bitsList:
      if i < 8:
        self.lcd_send_byte(bits, LCD_CHR)
      i += 1
    self._newCharacters[name] = position
  
  def getNewCharacter(self, name):
    newCharHex = self._newCharacters[name]
    if newCharHex is None:
      newCharHex = 0x00
    return newCharHex
  
  def simpleDemo(self):
    newCharacter1 = [0x04, 0x06, 0x04, 0x06, 0x04, 0x04, 0x0e, 0x0e]
    newCharacter2 = [0x04, 0x08, 0x0a, 0x12, 0x11, 0x11, 0x0a, 0x04]
    self.createOneNewCharacter("temperature", 1, newCharacter1)
    self.createOneNewCharacter("pressure", 1, newCharacter2)
    self.displayChar(1, [self.getNewCharacter("temperature")], " simple demo")
    self.displayChar(2, [self.getNewCharacter("pressure")], " for LCD1602")
    while True:
      self.displayCharFromPosition(1, 14, "10")
      self.displayCharFromPosition(2, 13, "50%")
      time.sleep(3)
      self.displayCharFromPosition(1, 14, "25")
      self.displayCharFromPosition(2, 13, "90%")
      time.sleep(3)
