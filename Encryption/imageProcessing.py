##
#  This program hide or find a message in a digital BMP file.
#  Designed by Charmaine Yuen.
#

from io import SEEK_CUR
from sys import exit

def main():
    # Ask the user for the bmp file.
    imgName = input("What is the image file? ")
    imgFile = open(imgName, "rb+")
    # User choose
    choice = input("Do you want to hide of find a message? H/F: ")
    if choice == "H":
        # Extract the image information.
        fileSize = readInt(imgFile, 2)
        start = readInt(imgFile, 10)
        width = readInt(imgFile, 18)
        height = readInt(imgFile, 22)
        # Scan lines must occupy multiples of four bytes.
        scanlineSize = width * 3
        if scanlineSize % 4 == 0:
            padding = 0
        else:
            padding = 4 - scanlineSize % 4
        # Make sure this is a valid image.
        if fileSize != (start + (scanlineSize + padding) * height):
            exit("Not a 24-bit true color image file.")

        # Hide the message into the bmp file.
        hideMessage(50, 100, 49, imgFile, getASCII("encrypted.txt"))

    elif choice == "F":
        # Ask user for the embed information.
        startingPoint = int(input("What is the starting point? "))
        skipSize = int(input("What is the skip size? "))
        textSize = int(input("What is the text size? "))
        color = input("What is the color? ")
        findMessage(startingPoint, skipSize, textSize, imgFile, color)

    # CLose the bmp file.
    imgFile.close()

## Gets an integer from a binary file. (Provided by the book)
#  @param imgFile the file
#  @param offset the offset at which to read the integer
#  @return the integer starting at the given offset
#
def readInt(imgFile, offset):
    # Move the file pointer to the given byte within the file.
    imgFile.seek(offset)
    # Read the 4 individual bytes and build an integer.
    theBytes = imgFile.read(4)
    result = 0
    base = 1
    for i in range(4):
        result = result + theBytes[i] * base
        base = base * 256
    return result

## Read from the encrypted txt file and change it into ascii numbers.
#  @param txt file
#  @return a list of ascii numbers.
#
def getASCII(txtFile):
    asciiMessage = []
    inputFile = open(txtFile, "r")
    for line in inputFile:
        for char in line:
            asciiMessage.append(ord(char))
    inputFile.close()
    return asciiMessage

## Processes an individual pixel.
#  @param imgFile, the BMP file
#  @param asciiNumber, the ascii number to change the byte
#  @return through the BMP file.
#
def processPixel(imgFile, asciiNumber):
    # Read the pixel as individual bytes.
    theBytes = imgFile.read(3)
    blue = theBytes[0]
    green = theBytes[1]
    # Process the pixel.
    newRed = asciiNumber
    # Write the pixel.
    imgFile.seek(-3, SEEK_CUR)  # Go back 3 bytes to the start of the pixel
    imgFile.write(bytes([blue, green, newRed]))


## Embed the message into a BMP file.
#  Uses processPixel.
#  @param startingPoint, skipSize, textSize are integers.
#  @param imageFile is the BMP file
#  @param asciiMessage is a list of ascii numbers which is obtained in getASCII.
def hideMessage(startingPoint, skipSize, textSize, imageFile, asciiMessage):
    for i in range(textSize):
        imageFile.seek(startingPoint + skipSize * i)
        processPixel(imageFile, asciiMessage[i])

## Get an individual ASCII number.
#  @param imgFile, the BMP file
#  @param color, depends on the RGB color that the message is embedded into.
#  @return asciiNumber is the individual ASCII number.
#
def readASCII(imageFile, color):
   # Read the 4 individual bytes and build an integer.
   theBytes = imageFile.read(3)
   if color == "blue":
       asciiNumber = theBytes[0]
   elif color == "green":
       asciiNumber = theBytes[1]
   elif color == "red":
       asciiNumber = theBytes[2]
   return asciiNumber

## Find the message from a BMP file.
#  Uses readASCII.
#  @param startingPoint, skipSize, textSize are integers.
#  @param imageFile is the BMP file
#  @param color, depends on the RGB color that the message is embedded into.
#  Output the encrypted message into "output.txt"
def findMessage(startingPoint, skipSize, textSize, imageFile, color):
    outFile = open("output.txt", "w")
    for i in range(textSize):
        imageFile.seek(startingPoint + skipSize * i)
        encryptedChar = chr(readASCII(imageFile, color))
        outFile.write(encryptedChar)
    outFile.close()

# Start the program.
main()