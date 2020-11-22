## user defined settings
starting_xp = 13372
resolution = "1920x1080"

##########

### code starts here ###
import time, ctypes
from python_imagesearch.imagesearch import imagesearch
from datetime import datetime

## using python to send keypresses
# as per EDIT2 https://www.reddit.com/r/learnpython/comments/22tke1/use_python_to_send_keystrokes_to_games_in_windows/
# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

SendInput = ctypes.windll.user32.SendInput

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def TapSpace():
    PressKey(0x39)
    time.sleep(.05)
    ReleaseKey(0x39)

def TapEsc():
    PressKey(0x01)
    time.sleep(.05)
    ReleaseKey(0x01)

## using win32 to get/set cursor position & window, and the handle for the Fall Guys client
# https://programtalk.com/vs2/python/12682/dragonfly/dragonfly/actions/action_mouse.py/
# https://docs.microsoft.com/en-us/windows/win32/

class _point_t(ctypes.Structure):
    _fields_ = [
                ('x',  ctypes.c_long),
                ('y',  ctypes.c_long),
               ]

def GetCursor():
    point = _point_t()
    cursor = ctypes.windll.user32.GetCursorPos(ctypes.pointer(point))
    if cursor:  return (point.x, point.y)
    else:       return None
 
def SetCursor(x, y):
    result = ctypes.windll.user32.SetCursorPos(ctypes.c_long(int(x)), ctypes.c_long(int(y)))
    if result:  return False
    else:       return True

def GetWindow():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if hwnd:    return (hwnd)
    else:       return None

def SetWindow(hwnd):
    while True:
        if ctypes.windll.user32.SetForegroundWindow(hwnd):
            break

## get the handle for the Fall Guys client window
FG_hwnd = ctypes.windll.user32.FindWindowW(None,"FallGuys_client")

## use imagesearch to find image called name, can fail if file doesn't exist, or if image isn't found
# https://brokencode.io/how-to-easily-image-search-with-python/
def FindImage(name):
    if not name.endswith(".png"):  name += ".png"
    file = "images/" + resolution + "/" + name
    try:
        location = imagesearch(file)
        return location if location[0] != -1 else False
    except: return False

## send key to Fall Guys client
def SendToFG(key=None):
    mouse = GetCursor()
    current_hwnd = GetWindow()
    SetWindow(FG_hwnd)
    if key == "space":
        TapSpace()
    elif key == "esc":
        TapEsc()
    else:
        pass
    SetWindow(current_hwnd)
    SetCursor(mouse[0],mouse[1])

## Look for image and send key if successful
def CheckFor(name, key=None):
    if FindImage(name):
        SendToFG(key)
        return True
    else:
        return False

## Wait for loop
def WaitFor(trigger, key, attempts):
    for attempt in range (attempts):
        if CheckFor(trigger, key):
            return True
    return False

## sub loops
sub_loops = [
    ("lobby","space",10),
    ("mainshow",None,100),
    ("populating",None,250),
    ("waiting",None,500),
    ("qualified",None,250),
    ("exit","esc",2500),
    ("exitshow","space",10),
    ("results","space",10),
    ("close","space",10),
    ("confirm","space",10)
    ]

## logger
def Logger(logtext):
    logline = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - "
    logline += logtext
    print(logline)
    f = open("log.txt", "a")
    f.write(logline + "\n")
    f.close()

## experience tracking
current_xp = starting_xp
def IncrementScore():
    global current_xp
    current_xp += 15

## main loop
# iterator
def DoLoops():
    for trigger, key, attempts in sub_loops:
        Logger("Checking for " + str(trigger))
        check = "Check for " + str(trigger)
        if not WaitFor(trigger, key, attempts):
            Logger(check + " failed")
            if trigger == "populating":
                Logger("Checking for connection error")
                if WaitFor("connectionerror","space",10):
                    TapEsc
                    time.sleep(1)
                    TapSpace
                    break
                break
        else:
            Logger(check + " succeeded")
            if trigger == "confirm":
                IncrementScore()
                Logger("current_xp = " + str(current_xp))

# loop
while True:
    DoLoops()
    if current_xp > 40000:
        break
