from time import localtime, strftime, sleep

format = 0
formats = ["%H:%M:%S", "%H:%M", "   %d.%m\n%H:%M:%S"]

def nextTickWait(coords, page, serial) :
    return 1 #Time until next tick in seconds

def getKeyState(coords, page, serial, action) :
    if action == "clock" :
        return {"caption": strftime(formats[format], localtime()),
                "fontSize": 12,
                "fontColor": "black",
                "actions": {}}

def keyPress(coords, page, serial) : #Cycle through time formats on keypress
    global format
    format += 1

    if format+1 > len(formats) :
        format = 0

#print("Hello, world!")

if __name__ == "__main__" :
    print(getKeyState("0x0", "clock"))    