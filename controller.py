from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont
import importlib
import uuid
import json
import math
import time
import sys
import os

class button :
    def __init__(self, keyIndex, controller) :
        self.controller = controller
        self.keyIndex = keyIndex

        #Get the coords of the button. (Top left button is 0x0.)
        self.x = (keyIndex % controller.width)
        self.y = math.ceil((keyIndex+1) / controller.width)-1

        self.coords = f"{self.x}x{self.y}"

        self.caption = ""
        self.fontSize = 14
        self.fontColor = "white"
        self.activated = False
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
        if not self.activated :
            size = 0
        else :
            size = round(self.controller.buttonRes / 6)

        image = PILHelper.create_scaled_image(self.controller.deck, self.background, margins=[size, size, size, size])

        draw = ImageDraw.Draw(image)
        
        fontSize = self.fontSize
        if self.activated :
            fontSize = fontSize / 1.25

        font = ImageFont.truetype(self.font, round(fontSize)) #Also resizing the text over here
        draw.text((image.width / 2, image.height / 2), text=self.caption, font=font, anchor="ms", fill=self.fontColor)

        image = PILHelper.to_native_format(self.controller.deck, image)

        with self.controller.deck :
            self.controller.deck.set_key_image(self.keyIndex, image)
    
    def loadImage(self, path) :
        self.background = Image.open(path)
    
    def coordsCaption(self) :
        self.caption = f"{self.keyIndex} - {self.coords}"

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
    
    def setKeyCallback(self, func) :
        self.deck.set_key_callback(func)
    
    def coordsCaptions(self) :
        for key in self.screen :
            self.screen[key].coordsCaption()

class pages :
    def __init__(self, controller) :
        self.pages = {}
        self.images = {}
        self.ticks = {}

        self.activePage = {}
        self.activePageName = ""

        self.tickingItems = {}

        self.controller = controller
        self.controller.setKeyCallback(self.clickHandler)

        for page in os.listdir("pages") : #Load all the .json files to memory
            if page.endswith(".json") :
                with open(os.path.join("pages", page), "r") as f :
                    self.pages[page] = json.loads(f.read())
        
        for page in self.pages : #Load all the used images to memory
            for image in self.pages[page]["images"] :
                if not image in self.images :
                    path = os.path.join("pages", "imgs", image)

                    if os.path.isfile(path) :
                        self.images[image] = Image.open(path)
                    else :
                        print(f"{image} not found!")
                        self.images[image] = Image.new("RGB", (self.controller.buttonRes, self.controller.buttonRes))
            
            for tick in self.pages[page]["ticks"] : #Imports all the ticking files
                name = tick.strip(".py")
                id = "t" + uuid.uuid4().hex[:12]
                
                #exec(f"global {id}") #Trying to import the module using diffrent methods
                #exec(f"import pages.ticks.{name} as {id}")

                #module = __import__(f"pages.ticks.{name}")
                #print(module)
                #globals()[id] = module

                module = importlib.import_module(f"pages.ticks.{name}")
                globals()[id] = module

                self.ticks[tick] = id
                
    
    def switchToPage(self, page) :
        j = self.pages[page]
        buttons = j["buttons"]

        self.controller.resetScreen()
        #self.controller.coordsCaptions()
        
        self.activePage = j
        self.activePageName = page

        self.tickingItems = {}

        for button in buttons :
            buttonJ = buttons[button]

            key = self.controller.screen[button]
            key.setCaption(buttonJ["caption"])
            key.background = self.images[buttonJ["background"]]
            key.fontSize = buttonJ["fontSize"]
            key.fontColor = buttonJ["color"]

            if "ticks" in buttonJ :
                #self.tickingItems[button] = "hello"
                t = {}

                for tick in buttonJ["ticks"] :
                    t[tick] = {"action": buttonJ["ticks"][tick], "lastTrigger": 0, "nextTrigger": 0}
                
                self.tickingItems[button] = t
        
        #print(self.tickingItems)

        #self.tick()
        self.controller.sendScreenToDevice()
    
    def triggerAction(self, coords, action, actionData) :
        print(coords, action, actionData)

        if action == "switchPage" :
            self.switchToPage(actionData)
        elif action == "exit" :
            self.controller.deck.reset()
            self.controller.deck.close()
            sys.exit()
    
    def clickHandler(self, deck, keyIndex, state) :
        x = (keyIndex % self.controller.width)
        y = math.ceil((keyIndex+1) / self.controller.width)-1
        coords = f"{x}x{y}"

        self.controller.screen[coords].activated = state #Triggers the click 'animation'.
        self.controller.screen[coords].sendToDevice()

        if not state : #Wait until the button is released
            try :
                button = self.activePage["buttons"][coords]
            
                for action in button["actions"] :
                    actionData = button["actions"][action]
                    self.triggerAction(coords, action, actionData)

                if coords in self.tickingItems : #Triggers tick function on ticking buttons
                    ticks = self.tickingItems[coords]
                    
                    for tick in ticks :
                        tickID = self.ticks[tick]

                        tickModule = globals()[tickID]
                        tickModule.keyPress(coords, self.activePageName, self.controller.serial)


            except KeyError :
                pass
    
    def tick(self) :
        for button in self.tickingItems :
            ticks = self.tickingItems[button]
            for tick in ticks :
                tickID = self.ticks[tick]
                action = ticks[tick]["action"]
                nextTrigger = ticks[tick]["nextTrigger"]

                if time.time() > nextTrigger :

                    tickModule = globals()[tickID]

                    newState = tickModule.getKeyState(button, self.activePageName, self.controller.serial, action)
                    key = self.controller.screen[button]

                    if "caption" in newState :
                        key.caption = newState["caption"]
                    
                    if "fontColor" in newState :
                        key.fontColor = newState["fontColor"]

                    if "fontSize" in newState :
                        key.fontSize = newState["fontSize"]
                    
                    if len(newState["actions"]) > 0 :
                        for action in newState["actions"] :
                            actionData = newState["actions"][action]
                            self.triggerAction(button, action, actionData)
                        self.controller.sendScreenToDevice()
                    else :
                        key.sendToDevice()
                    
                    ticks[tick]["nextTrigger"] = time.time() + tickModule.nextTickWait(button, self.activePageName, self.controller.serial) 


# ------------------------ #
def helloWorldTest() :
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks) :

        c = controller(deck)

        middleKey = c.screen["2x2"]
        middleKey.loadImage("test.png")
        middleKey.setCaption("Hello,\nworld!")
        middleKey.setFont("C:\\Windows\\Fonts\\Arial.ttf", size=15, color="red")

        c.sendScreenToDevice()

        while True :
            time.sleep(10)

# ------------------------ #
           
if __name__ == "__main__" :
    streamdecks = DeviceManager().enumerate()

    for index, deck in enumerate(streamdecks) :
        c = controller(deck)

        p = pages(c)
        p.switchToPage("page1.json")

        while True :
            time.sleep(.5)
            p.tick()