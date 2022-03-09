from StreamDeck.DeviceManager import DeviceManager
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
import threading
import time
import math
import sys 


streamdecks = DeviceManager().enumerate()
presses = 0
#print(len(streamdecks))

def setKeyImage(deck, key, path, text) :
    print("Setting image.")

    background = Image.open(path)
    image = PILHelper.create_scaled_image(deck, background, margins=[0, 0, 0, 0])

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 14)
    draw.text((image.width / 2, image.height / 2), text=text, font=font, anchor="ms", fill="white")


    image = PILHelper.to_native_format(deck, image)

    with deck :
        deck.set_key_image(key, image)

def keyPress(deck, key, state) :
    print(f"Key {key} is now {state}.")

    if state :
        setKeyImage(deck, key, "c.png", f"{key} (ON)")

        global presses
        presses = presses + 1
        setKeyImage(deck, 2, "a.png", f"{presses}")

    else :
        setKeyImage(deck, key, "b.png", f"{key} (OFF)")
    
    if key == 2 :
        deck.reset()
        deck.close()
        sys.exit()

for index, deck in enumerate(streamdecks):
    print(index, deck.deck_type())

    deck.open()
    deck.reset()

    deck.set_brightness(75)

    deck.set_key_callback(keyPress)

    for key in range(deck.key_count()) :
        print(f"Key: {key}")
        setKeyImage(deck, key, "b.png", f"{math.ceil((key+1)/5)} (OFFr)")
        time.sleep(.5)
    
    while True :
        time.sleep(1)

        #setKeyImage(deck, 2, "a.png", f"{presses}")