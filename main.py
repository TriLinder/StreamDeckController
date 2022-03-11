from StreamDeck.DeviceManager import DeviceManager
import controller
import time
import json
import sys
import os

def getConfigKey(key) : #Load a key from config.json
    if not os.path.isfile("config.json") :
        print("'config.json' not found.")
        input("Press [ENTER] to quit..")
        sys.exit()
    
    with open("config.json", "r") as f :
        j = json.loads(f.read())
    
    try :
        return j[key]
    except KeyError :
        print(f"'{key}' not found in config.json")
        input("Press [ENTER] to quit..")
        sys.exit()

def writeConfigKey(key, data) : #Write key to config.json
    if not os.path.isfile("config.json") :
        print("'config.json' not found.")
        input("Press [ENTER] to quit..")
        sys.exit()
    
    with open("config.json", "r") as f :
        j = json.loads(f.read())
    
    j[key] = data

    with open("config.json", "w") as f :
        json.dump(j, f)

    
def chooseDevice(devices) : #Select device
    print("Please choose your device:")

    serials = []

    i = 0
    for device in devices :
        i += 1

        device.open()

        type = device.deck_type()
        serial = device.get_serial_number()

        device.close()

        serials.append(serial)

        print(f"    {i}. {type} ({serial})")

    selection = input("Option: ").strip()

    try :
        selection = int(selection)
    except :
        print("Not an integer.")
        input("Press [ENTER] to quit..")
        sys.exit()
    
    if selection not in range(1, len(serials)+1) :
        print("Not in range.")
        input("Press [ENTER] to quit..")
        sys.exit()
    
    serial = serials[selection-1]

    print("\nDevice selected.")
    if input("Would you like to save your selection? y/N ").lower().strip() == "y" :
        writeConfigKey("deviceSerial", serial)
        print("Option saved.")
    
    return serial


if __name__ == "__main__" :
    #print("Starting..")

    startingPage = getConfigKey("startingPage")
    startingBrighntess = getConfigKey("startingBrightness")
    deviceSerial = getConfigKey("deviceSerial")
    font = getConfigKey("font")

    if deviceSerial == "selectOnStartup" :
        deviceSerial = chooseDevice(DeviceManager().enumerate())
    
    streamdecks = DeviceManager().enumerate()

    for deck in streamdecks :
        deck.open()
        
        if deck.get_serial_number() == deviceSerial :
            deck.close()
            
            c = controller.controller(deck, font=font)
            deck.set_brightness(startingBrighntess)

            p = controller.pages(c)
            p.switchToPage(startingPage)

            while True :
                time.sleep(.25)
                p.tick()

        deck.close()
    
    print(f"Stream Deck device with the serial '{deviceSerial}' was not found.")