import sys
import time

from actions import *


class Bot:
    def __init__(self, box, params):
        self._running = True
        self.box = box
        
        self.confidence = params['confidence']
        self.max_targets = params['max_targets']
        self.min_ores = params['min_ores']
        self.min_ores_locked = params['min_ores_locked']
        self.t_approach = params['t_approach']
        self.t_check = params['t_check']
        self.t_mine = params['t_mine']
        self.t_station2 = params['t_station2']
        self.t_station3 = params['t_station3']
        self.t_undock = params['t_undock']
        self.t_warp = params['t_warp']
        
    def stop(self):
        self._running = False
    
    def run(self):
        load = 0
        while self._running:
            # Initialization: Bring out eye (and asteroid filter if currently mining)
            t_mine = 0
            while t_mine < self.t_mine and not Full_Capacity(confidence=self.confidence, box=self.box):
                if Locked_Ores_Less_Than(self.min_ores_locked, confidence=self.confidence, box=self.box):
                    while Ores_Less_Than(self.min_ores, confidence=self.confidence, box=self.box):
                        To_Random_Signal(self.t_warp, box=self.box)
                    Approach(self.t_approach, confidence=self.confidence, box=self.box)
                    Mine(self.max_targets, confidence=self.confidence, box=self.box)
                for i in range(self.t_check):
                    time.sleep(1)
                    t_mine += 1
                    text = 'Total Elapsed Mining Time:' + str(t_mine) + '/' + str(self.t_mine)
                    sys.stdout.write('\r' + text)
                    sys.stdout.flush()
                print()
            To_Station(STATION2, SHORTCUT1, False, self.t_station2, box=self.box)
            Unload_And_Stack_All(confidence=self.confidence, box=self.box)
            load += 1
            print('Loads:', load)
            print('-'*13)
            To_Station(STATION3, None, True, self.t_station3, box=self.box)
            Undock(self.t_undock, box=self.box)
            Click_Eye(box=self.box)
            
            