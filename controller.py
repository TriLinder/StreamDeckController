from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont
import math
import time

class button :
    def __init__(self, keyIndex, controller) :
        self.keyIndex = keyIndex

        #Get the coords of the button. (Top left button is 0x0.)
        self.x = (keyIndex % controller.width)
        self.y = math.ceil((keyIndex+1) / controller.width)

        self.coords = f"{self.x}x{self.y}"

        self.caption = f"{self.keyIndex} - {self.coords}"
        self.fontSize = 14
        self.fontColor = "white"
        self.font = "C:\\Windows\\Fonts\\Arial.ttf"

        self.background = Image.new("RGB", (controller.buttonRes, controller.buttonRes))
    
    def setCaption(self, caption) :
        self.caption = str(caption)

    def setFont(self, font, size=None, color=None) :
        self.font = font

        if size :
            self.fontSize = size
        
        if color :
            self.fontColor = color

    def sendToDevice(self) :
        image = PILHelper.create_scaled_image(deck, self.background, margins=[0, 0, 0, 0])

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font, self.fontSize)
        draw.text((image.width / 2, image.height / 2), text=self.caption, font=font, anchor="ms", fill=self.fontColor)

        image = PILHelper.to_native_format(deck, image)

        with deck :
            deck.set_key_image(self.keyIndex, image)
    
    def loadImage(self, path) :
        self.background = Image.open(path)

class controller :
    def __init__(self, deck) :
        self.deck = deck

        deck.open()
        deck.reset()

        self.keyCount = deck.key_count()
        self.height = deck.key_layout()[0]
        self.width = deck.key_layout()[1]
        self.serial = deck.get_serial_number()
        self.buttonRes = deck.key_image_format()["size"][0] #The resolution of a single button

        self.resetScreen()

    def resetScreen(self) :
        d = {}

        for key in range(self.keyCount) :
            btn = button(key, self)
            d[btn.coords] = btn
        
        self.screen = d
    
    def sendScreenToDevice(self) :
        for key in self.screen :
            self.screen[key].sendToDevice()

if __name__ == "__main__" :
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks) :

        c = controller(deck)

        middleKey = c.screen["2x2"]
        middleKey.loadImage("test.png")
        middleKey.setCaption("Hello, world!")
        middleKey.setFont("C:\\Windows\\Fonts\\Arial.ttf", size=12, color="red")

        c.sendScreenToDevice()

        while True :
            time.sleep(10)