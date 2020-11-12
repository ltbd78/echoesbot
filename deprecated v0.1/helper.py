import pyautogui
import random
import time
import sys
import numpy as np
import copy

from coords import *


def rclick(coords, subitem_n=None, n=2, y_offset=Y_OFFSET, t=1, padding=.25, verbose=False):
    """
    coords is [x1, y1, x2, y2] where (x1, y1) is top left corner and (x2, y2) is bottom right corner
    n is the number of emulators
    y_offset is the emulator vertical offset
    subitem is predefined (TODO: make relative position)
    """
    def pause(t):
        t = int(t + random.gauss(.1*t, .1*t/3))
        time.sleep(t)
    
    coords = copy.deepcopy(coords)
    
    for i in range(n):
        coords[1] = coords[1] + i*y_offset
        coords[3] = coords[3] + i*y_offset
        assert(padding < .5)
        dx = coords[2] - coords[0]
        dy = coords[3] - coords[1]
        x = round(random.uniform(coords[0] + padding*dx, coords[2] - padding*dx))
        y = round(random.uniform(coords[1] + padding*dy, coords[3] - padding*dy))
        pyautogui.click(x, y)
        if verbose:
            print('coords:', x, y)
        pause(t)
        
        if subitem_n is not None: # TODO
            dx = SUBITEM00[2] - SUBITEM00[0]
            dy = SUBITEM00[3] - SUBITEM00[1]
            _, y = pyautogui.position()
            x = random.uniform(SUBITEM00[0] + padding*dx, SUBITEM00[2] - padding*dx)
            y = y + dy*subitem_n
            pyautogui.click(x, y)
            if verbose:
                print('subitem', x, y)
            pause(t)

    
def print_status(s):
    sys.stdout.write(s)
    sys.stdout.flush()

    
def wait(t, text):
    t = int(t + random.gauss(.1*t, .1*t/3))
    for i in range(t):
        time.sleep(1)
        print_status('\r' + text + ' ' + str(i+1) + '/' + str(t))
    print()