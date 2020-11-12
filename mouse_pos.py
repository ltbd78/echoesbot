import pyautogui
import sys
import time

while True:
    pos = str(pyautogui.position())
    sys.stdout.write('\r' + pos)
    sys.stdout.flush()
    time.sleep(0.01)