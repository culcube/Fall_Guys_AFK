## user defined settings
starting_xp = 13132
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
def WaitFor(trigger, key, attempts, check=None):
    for attempt in range (attempts):
        if CheckFor(trigger, key):
            if check != None:
                for attempt2 in range (attempts):
                    if CheckFor(trigger):
                        return True
                return False
            return True
    return False


## Main Loop
# sub loops
def Lobby():
    if WaitFor("lobby","space",10,"mainshow"):
        return True
    return False

def Populating():
    if WaitFor("mainshow",None,100,"populating"):
        return True
    return False

def GamePicked():
    if WaitFor("waiting",None,250,"qualified"):
        return True
    return False

def GameStart():
    if WaitFor("qualified",None,100):
        return True
    return False

def RoundOver():
    if WaitFor("exit","esc",500):
        return True
    return False

def ExitShow():
    if WaitFor("exitshow","space",10):
        return True
    return False

def Results():
    if WaitFor("results","space",10,"lobby"):
        return True
    return False

## experience tracking
current_xp = starting_xp
def IncrementScore():
    global current_xp
    cuurent_xp += 15

while True:
    if not Lobby():
        print ("Lobby failed")
        break
    if not Populating():
        print ("Populating failed")
        break
    if not GamePicked():
        print ("GamePicked failed")
        break
    if not GameStart():
        print ("GameStart failed")
        break
    if not RoundOver():
        print ("RoundOver failed")
        break
    if not ExitShow():
        print ("ExitShow failed")
        break
    if not Results():
        print("Results failed")
        break
    IncrementScore()
    print ("current_xp")
