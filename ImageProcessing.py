# LSB Method
from PIL import Image
import time

message = input("Type a hidden message: ")
file = input("Type an image name (e.g. photo.png): ")
codedFile = "coded.png"


def codeAMessage(file, message):
    messageBinary = []
    index = 0
    newpixelsdata = []

    # MESSAGE STORED AS ONE SEQUENCE OF BITS
    for i in message:
        messageBinary.append("{:08b}".format(ord(i)))
    messageBits = ''.join(messageBinary)

    print("1. Opening image")
    image = Image.open(file)
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    image.show()

    time.sleep(3)

    # STORE PIXELS DATA IN imagePixelData
    print("2. Getting pixels from image")
    imagePixelData = list(image.getdata())
    width, height = image.size
    binaryPixels = []

    print("3. Converting pixels decimal values into binary")
    for x in range(width*height):
        pixel = list(imagePixelData[x])
        row = []
        for i in range(4):
            row.append("{:08b}".format(pixel[i]))
        binaryPixels.append(row)

    print("4. Changing pixel value")
    for pixel in binaryPixels:
        for i in range(3):
            if index < len(messageBits):
                colorBinary = list(pixel[i])
                colorBinary[-1] = messageBits[index]
                pixel[i] = ''.join(colorBinary)
                index += 1
            else:
                break
        if index >= len(messageBits):
            break

    for i in range(len(binaryPixels)):
        newpixelsdata.append((
            int(binaryPixels[i][0], 2),
            int(binaryPixels[i][1], 2),
            int(binaryPixels[i][2], 2),
            int(imagePixelData[i][3])
        ))

    print("5. Creating a new image\n")
    newimage = Image.new(mode="RGBA", size=(width, height))
    newimage.putdata(newpixelsdata)
    newimage.show()
    newimage.save('coded.png')


def decodeAMessage(file):
    image = Image.open(file)

    imagePixelData = list(image.getdata())
    width, height = image.size
    binaryPixels = []

    for x in range(width*height):
        pixel = list(imagePixelData[x])
        row = []
        for i in range(4):
            row.append("{:08b}".format(pixel[i]))
        binaryPixels.append(row)

    decodedBits = ''
    for pixel in binaryPixels:
        for i in range(3):
            decodedBits += pixel[i][-1]

    # READ A MESSAGE FROM BITS
    decodedMessage = ''.join(
        [chr(int(decodedBits[i:i+8], 2)) for i in range(
            0, len(decodedBits), 8)])
    print("Decoded message:", decodedMessage)

    if decodedMessage.startswith(message):
        print("\nMessage successfully hidden and decoded!")
    else:
        print("\nDecoded message does not match the original.")


codeAMessage(file, message)
decodeAMessage(codedFile)
