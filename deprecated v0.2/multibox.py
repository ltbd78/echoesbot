import pyautogui
import random
import sys
import time
import copy


def pause(t, text=None):
    t = int(t + random.gauss(.1*t, .1*t/3))
    if text is not None:
        for i in range(t):
            sys.stdout.write('\r' + text + ' ' + str(i+1) + '/' + str(t))
            sys.stdout.flush()
            time.sleep(1)
        print()
    else:
        time.sleep(t)


class MultiBox:
    def __init__(self, size, locs):
        """
        size := size of all boxes i.e. `(960, 600)`
        locs := a list of top-left coords of boxes i.e. `[(0, 0), (0, 600)]`
        """
        self.size = size
        self.locs = locs
    
    def click(self, coords0, t=1, padding=.5, verbose=False, box=None):
        """
        coords0 := the coordinate of buttons mapped with (0, 0) as reference i.e. `np.array([x1, y1, x2, y2])`
        box := index of self.locs i.e. `0`
        t := time delay with randomness
        padding := inner padding of buttons to avoid mapping errors
        verbose: prints coords
        """
        assert(coords0[2] > coords0[0]) # x2 > x1
        assert(coords0[3] > coords0[1]) # y2 > y1
        assert(padding < 1)

        dx = coords0[2] - coords0[0]
        dy = coords0[3] - coords0[1]
        
        coords = copy.deepcopy(coords0)
        if box is not None:
            coords[0] += self.locs[box][0] # x offset
            coords[1] += self.locs[box][1] # y offset
            coords[2] += self.locs[box][0] # x offset
            coords[3] += self.locs[box][1] # y offset

        x = round(random.uniform(coords[0] + dx*padding/2, coords[2] - dx*padding/2))
        y = round(random.uniform(coords[1] + dy*padding/2, coords[3] - dy*padding/2))
        
        pyautogui.click(x, y)

        if verbose:
            print('coords:', x, y)

        pause(t)
    
    def in_box(self, coord, box):
        box_coord = [self.locs[box][0], self.locs[box][1],
                     self.locs[box][0] + self.size[0], self.locs[box][1] + self.size[1]]
        
        if box_coord[0] < coord[0] < coord[2] < box_coord[2]:
            if box_coord[1] < coord[1] < coord[3] < box_coord[3]:
                return True
        
        return False
    
    def locate(self, png, confidence, box):
        """
        Returns all absolute coords of detected PNG within a given box
        READ: When passed in to click(), make sure box=None as it is an absolute coordinate!
        """
        coords = []
        for i in pyautogui.locateAllOnScreen(png, confidence=.87):
            coord = [i.left, i.top, i.left + i.width, i.top + i.height]
            if self.in_box(coord, box):
                coords.append(coord)
        
        return coords
            