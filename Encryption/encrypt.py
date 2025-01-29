##
#  This program encrypts a file using the Vigenère cipher.
#  Modified from Program 7.7.1: cipher.py. by Charmaine Yuen
#

from sys import argv
DEFAULT_KEY = "piano"

def main():
    key = DEFAULT_KEY
    infile = ""
    outfile = ""
    files = 0  # Number of command line arguments that are files.
    for i in range(1, len(argv)):
        arg = argv[i]
        if arg[1] == "-":
            # It is a command line option.
            option = arg[2]
            if option == "d":
                key = invertKey(key)
        else:
            # It is a file name.
            files = files + 1
            if files == 1:
                infile = arg
            elif files == 2:
                outfile = arg

    # There must be two files.
    if files != 2:
       usage()
       return

    # Open the files.
    inputFile = open(infile, "r")
    outputFile = open(outfile, "w")

    # Read the characters from the file.
    keyIndex = 0
    for line in inputFile:
        for char in line:
            newChar = encrypt(char, key[keyIndex])
            keyIndex = (keyIndex + 1) % len(key)
            outputFile.write(newChar)

    # Close the files.
    inputFile.close()
    outputFile.close()

## Inverts the key for decryption.
#  @param key the original key
#  @return the inverted key
#
def invertKey(key):
    LETTERS = 26  # Number of letters in the Roman alphabet.
    keyInverted = ""
    for char in key:
        keyInverted += chr((LETTERS - (ord(char) - ord('a'))) % LETTERS + ord('a'))
    return keyInverted

## Encrypts upper and lowercase characters using a Vigenère cipher.
#  @param ch the letter to be encrypted
#  @param keyChar the character from the key
#  @return the encrypted letter
#
def encrypt(ch, keyChar):
    LETTERS = 26  # Number of letters in the Roman alphabet.
    if ch.isalpha():
        base = ord('a')
        if ch.isupper():
            base = ord('A')
        offset = (ord(ch) - base + ord(keyChar.lower()) - ord('a')) % LETTERS
        return chr(base + offset)
    else:
        return ch  # Not a letter.

## Prints a message describing proper usage.
#
def usage():
    print("Usage: python vcipher.py [-d] infile outfile")

# Start the program.
main()