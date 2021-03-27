def convertToHEXForChar(charList):
    convertedCharList = []
    for message in charList:
      convertedCharList.append(ord(message))
    return convertedCharList
  
def displayChar(line, *args):
  concatedList = []
  for argItem in args:
    concatedList.extend(argItem)

  print(len(concatedList))
  for message in concatedList:
    print(message)

def main():
  displayChar(0, [0x00], convertToHEXForChar("! Rasbperry Pi"))

main()