from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont
import math
import time

class button :
    def __init__(self, keyIndex, controller) :
        self.keyIndex = keyIndex

        #Get the coords of the button. (Top left button is 0x0.)
        self.x = (keyIndex % controller.width) -1
        self.y = math.ceil(keyIndex / controller.width)

        self.caption = "test"
        self.background = Image.new("RGB", (controller.buttonRes, controller.buttonRes))
    
    def setCaption(self, caption) :
        self.caption = str(caption)

    def sendToDevice(self) :
        image = PILHelper.create_scaled_image(deck, self.background, margins=[0, 0, 0, 0])

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 14)
        draw.text((image.width / 2, image.height / 2), text=self.caption, font=font, anchor="ms", fill="white")

        image = PILHelper.to_native_format(deck, image)

        with deck :
            deck.set_key_image(self.keyIndex, image)

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
            d[key] = button(key, self)
        
        self.screen = d
    
    def sendScreenToDevice(self) :
        for key in self.screen :
            self.screen[key].sendToDevice()

if __name__ == "__main__" :
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks) :
        c = controller(deck)
        c.sendScreenToDevice()

        while True :
            time.sleep(10)