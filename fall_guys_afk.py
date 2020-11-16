
# https://brokencode.io/how-to-easily-image-search-with-python/
from python_imagesearch.imagesearch import imagesearch
import os
import time
from datetime import datetime

safety_check = 0
normal_check = 0
emergency_check = 0
starting_xp = 4111
current_xp = starting_xp

def check():
  if imagesearch("./populating.png")[0] != -1:
    print("waiting for show to start")
    time.sleep(20)
    check_clear()
  elif imagesearch("./exit.png")[0] != -1:
    global current_xp
    current_xp = current_xp + 15
    xp = str(current_xp)
    logline = "Round end at " + datetime.now().strftime("%H:%M:%S") + ", xp=" + xp
    print(logline)
    f = open("log.txt", "a")
    f.write(logline)
    f.close()
    escaping()
  elif any(map(lambda name: imagesearch("./" + name + ".png")[0]!=-1,
             ("OK", "OK2", "confirm", "close", "play"))):
    print("Passed!")
    global emergency_check
    emergency_check = 0
    global normal_check
    normal_check = 1

def escaping():
  print("escaping...")
  os.system("esc.ahk")
  print("Waiting for a moment...")
  time.sleep(0.5)
  print("Pressing space...")
  os.system("space.ahk")
  check_clear()

def check_clear():
  print("Clearing checks")
  global emergency_check
  emergency_check = 0
  global safety_check
  safety_check = 0
  global normal_check
  normal_check = 0

while True:
  safety_check = safety_check + 1
  counter = str(safety_check)
  print("check " + counter + ":")
  check()
  if current_xp > 40000:
    break
  elif safety_check == 0:
    print("All checks cleared")
    pass
  elif emergency_check > 1:
    print("Emergency!!! Escaping...")
    escaping()
    print("Sleeping for 5 minutes...")
    time.sleep(300)
  elif normal_check == 1:
    print("check " + counter + " passed, pressing space...")
    os.system("space.ahk")
    check_clear()
  elif safety_check > 59:
    print(counter + " checks failed, pressing space...")
    emergency_check = emergency_check + 1
    os.system("space.ahk")
    safety_check = 0
  else:
    print ("check " + str(safety_check) + " failed, sleeping...")
    time.sleep(0.5)
