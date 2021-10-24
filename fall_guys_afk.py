RepoURL = "http://github.com/culcube/Fall_Guys_AFK/"
RepoBranch = "main"

## Imports
import ctypes, shutil, subprocess, time
from datetime import datetime
from pathlib import Path
from urllib import request
### code requires image-search ###
try:
    from python_imagesearch.imagesearch import imagesearch
except:
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-imagesearch"])
    from python_imagesearch.imagesearch import imagesearch

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

def Tap(Key):
    PressKey(Key)
    time.sleep(0.5)
    ReleaseKey(Key)

# set some objects
SendInput = ctypes.windll.user32.SendInput
SpaceKey = 0x39
EscKey = 0x01

## using win32 to get/set cursor position & window
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

## send key to Fall Guys client and reset window + mouse cursor
def SendToFG(key=None):
    mouse = GetCursor()
    current_hwnd = GetWindow()
    SetWindow(FG_hwnd)
    Tap(key)
    SetWindow(current_hwnd)
    SetCursor(mouse[0],mouse[1])

## start FG from Steam folder
def StartFallGuys():
    global FG_hwnd
    subprocess.call(['C:\Program Files (x86)\Steam\steamapps\common\Fall Guys\FallGuys_client_game.exe'])
    while (FG_hwnd == 0):
        FG_hwnd = ctypes.windll.user32.FindWindowW(None,"FallGuys_client")
    time.sleep(15)
    SendToFG(SpaceKey)

## get the handle for the Fall Guys client window
try:
    FG_hwnd = ctypes.windll.user32.FindWindowW(None,"FallGuys_client")
except:
    StartFallGuys()

if not (FG_hwnd):
    StartFallGuys()

## get the resolution
def GetResolution():
    global resolution
    if not resolution:
        ResolutionObject = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(FG_hwnd, ctypes.pointer(ResolutionObject))
        height = ResolutionObject.bottom - ResolutionObject.top
        width = ResolutionObject.right - ResolutionObject.left
        # quick & dirty way to remove windowed borders.
        # screens are always a multiple of 10 pixels tall, but if windowed we need to remove the borders
        # if windowed there are 8 pixels at each edge for border
        # plus a further 23 pixels for the window title
        if height % 10 != 0:
            height -= 39
            width -= 16
        resolution = str(win_width) + "x" + str(win_height)
    return resolution

## ensure we have the necessary images for the resolution and dowload from repo as necessary
ImageFolder = 'images/'+GetResolution()+'/'
Path(ImageFolder).mkdir(parents=True, exist_ok=True)
if not RepoBranch.endswith("/"):  name += "/"
RepoImageFolder = RepoURL + "tree/" + RepoBranch + ImageFolder
RepoImageFolderScrape = request.urlopen(RepoImageFolder).readlines()
for line in RepoImageFolderScrape:
    html = str(line)
    if ImageFolder in html:
        array = html.split('"')
        filename = array[5]
        if not Path(ImageFolder + filename).exists():
            RepoImageFile = RepoURL + "raw/" + RepoBranch + ImageFolder + filename
            LocalFile = ImageFolder + filename
            with urllib.request.urlopen(RepoImageFile) as response, open(LocalFile, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

## use imagesearch to find image called name, can fail if file doesn't exist, or if image isn't found
# https://brokencode.io/how-to-easily-image-search-with-python/
def FindImage(name):
    if not name.endswith(".png"):  name += ".png"
    file = ImageFolder + name
    try:
        location = imagesearch(file)
        return location if location[0] != -1 else False
    except: return False

## Look for image (and send key if successful)
def CheckFor(name, key=None):
    if FindImage(name):
        print("check", name, "succeeded at", datetime.now())
        if (key):
            SendToFG(key)
            print("sent", key, "at", datetime.now())
        global CheckCounter
        CheckCounter += 2
        return True
    else:
        return False

## sub loops
Checks = [
    {"check": "mainshow",
     "key": SpaceKey},
    {"check": "lookingfor",
     "key": None},
    {"check": "populating",
     "key": None},
    {"check": "waitingforplayers",
     "key": None},
    {"check": "qualified",
     "key": None},
    {"check": "eliminated",
     "key": None},
    {"check": "exit",
     "key": EscKey},
    {"check": "exitshow",
     "key": SpaceKey},
    {"check": "showsummary",
     "key": None},
    {"check": "close",
     "key": SpaceKey},
    {"check": "confirm",
     "key": SpaceKey}
    ]

## Setting global values
# setting a counter for checks
CheckCounter = 0
# How many seconds before printing the same check
SilenceTime = 60
# How many periods of silence before aborting
AbortCounter = 3

## main loop
# iterator
def DoLoops():
    global CheckCounter
    if CheckCounter >= len(Checks):
        print("-=- Looping check reset at", datetime.now(), "-=-")
        CheckCounter = CheckCounter - len(Checks)
    CurrentCheck = Checks[CheckCounter]
    # We need to always be ready to see the next image, which requires us to start back at 0 when looking for the last image
    if CheckCounter == len(Checks)-1:
        NextCheck = Checks[0]
    else:
        NextCheck = Checks[CheckCounter+1]
    SilenceStart = time.time()
    Silenced = False
    AbortCheck = 0
    while not (CheckFor(NextCheck["check"], NextCheck["key"])):
        Checktime = time.time()
        TimeElapsed = Checktime - SilenceStart
        if TimeElapsed > SilenceTime:
            AbortCheck += AbortCheck
            if AbortCheck < AbortCounter:
                Silenced = False
                SilenceStart = time.time()
                print("still", end=" ")
            else:
                print("Aborting currect check by pressing Esc at", datetime.now())
                SendToFG(EscKey)
                # Find the first check that is expected after we press an Escape Key
                CheckCounter = Checks.index(next(x for x in Checks if x['key'] == EscKey)) + 1
                break
        else:
            if not Silenced:
                print("checking for:", CurrentCheck["check"], "at", datetime.now())
                Silenced = True
        if CheckFor(CurrentCheck["check"], CurrentCheck["key"]):
            CheckCounter -= 1
            break


print("Looper started at", datetime.now())
while True:
    DoLoops()
