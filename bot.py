import time

from coords import *
from multibox import *


class Bot:
    def __init__(self, multibox, box, params):
        self._running = True
        self.mb = multibox
        self.box = box
        
        self.confidence = params['confidence']
        self.drags = params['drags']
        self.max_targets = params['max_targets']
        self.min_ores = params['min_ores']
        self.min_ores_locked = params['min_ores_locked']
        self.ores = params['ores']
        self.signal = params['signal']
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
            while t_mine < self.t_mine and not self.Full_Capacity():
                if self.Locked_Ores_Less_Than(self.min_ores_locked):
                    while self.Ores_Less_Than(self.min_ores):
                        self.Warp_To_Signal(self.signal, 'names', None, self.t_warp)
                    if not self.Aquire_Target(self.ores, self.drags): # search & click items by priority
                        self.mb.click(self.box, ITEM1) # o.w. click item 1
                    self.Approach(self.t_approach)
                    self.Mine(self.max_targets)
                for i in range(self.t_check):
                    time.sleep(1)
                    t_mine += 1
                    
                    text = 'Total Elapsed Mining Time: ' + '{:02d}:{:02d}'.format(t_mine//60, t_mine%60)
                    print(text, end='\r')
                print()
            self.To_Station(SHORTCUT1, STATION2, False, self.t_station2)
            self.Unload_And_Stack_All()
            load += 1
            print('Loads:', load)
            print('-'*13)
#             self.To_Station(None, STATION3, True, self.t_station3)
            self.Undock(self.t_undock)
            self.Click_Eye()
            
    def change_box(self, box):
        self.box = box

    def _add_variance(self, coords, x1, y1, x2, y2):
        coords[0] -= x1 # adds width variance
        coords[1] -= y1 # adds height variance
        coords[2] += x2 # adds width variance
        coords[3] += y2 # adds height variance

    def _start_autopilot(self, confirm):
        print('Start Auto Pilot')
        self.mb.click(self.box, JUMP, t=2) # click jump
        self.mb.click(self.box, SETASDESTINATION) # set as destination
        self.mb.click(self.box, ABILITY1) # close map
        self.mb.click(self.box, X) # click X
        self.mb.click(self.box, STARTAUTOPILOT) # begin autopilot
        if confirm:
            self.mb.click(self.box, CONFIRM) # confirm if in station
    
    def Sort(self, by):
        self.mb.click(self.box, FILTER)
        self.mb.click(self.box, SORTBY)
        if by=='names':
            self.mb.click(self.box, NAMES)
        elif by=='distance':
            self.mb.click(self.box, DISTANCE)
        else:
            raise Exception('Invalid Sort Condition')
        self.mb.click(self.box, SMALLX)

    def Click_Eye(self):
        print('Clicking Eye')
        self.mb.click(self.box, EYE)

#     def To_Random_Signal(self, t_warp):
#         print('To Random Signal')
#         self.mb.click(self.box, DROPDOWN) # click dropdown menu
#         self.mb.click(self.box, DROPDOWN1)  # filter by signal

#         coords_signal = self.mb.locate(self.box, './PNG/asteroid.PNG', self.confidence)
#         i = random.randint(1, len(coords_signal)-1)
#         self._add_variance(coords_signal[i], 0, 10, 100, 10)
#         self.mb.click(None, coords_signal[i]) # click random signal (2:N)

#         coords_warp = self.mb.locate(self.box, './PNG/warp.PNG', self.confidence)
#         self._add_variance(coords_warp[0], 0, 10, 100, 10)
#         self.mb.click(None, coords_warp[0]) # warp

#         pause(t_warp, text='Warping') # wait
    
    def Warp_To_Signal(self, signal, sortby, idx, t_warp):
        print('To Signal')
        self.mb.click(self.box, DROPDOWN) # click dropdown menu
        self.mb.click(self.box, DROPDOWN1)  # filter by signal
        
        if sortby is not None:
            self.Sort(by=sortby)
        
        coords_signal = self.mb.locate(self.box, signal, self.confidence)
        print('Found', len(coords_signal), 'signals.')
        
        if idx is None:
            idx = random.randint(1, len(coords_signal)-1)
        
        print('Selecting index:', idx)
        coord = coords_signal[idx]
        self._add_variance(coord, -25, 5, 25, 5)
        self.mb.click(None, coord)
        
        coords_warp = self.mb.locate(self.box, './PNG/warp.PNG', self.confidence)
        self._add_variance(coords_warp[0], 0, 10, 100, 10)
        self.mb.click(None, coords_warp[0]) # warp

        pause(t_warp, text='Warping') # wait
        
        
    def Ores_Less_Than(self, n):
        self.mb.click(self.box, DROPDOWN) # click dropdown menu
        self.mb.click(self.box, DROPDOWN2) # filter by asteroid
        coords_ore_unlocked = self.mb.locate(self.box, './PNG/ore_unlocked.PNG', self.confidence)
        coords_ore_locked = self.mb.locate(self.box, './PNG/ore_locked.PNG', self.confidence)
        num = len(coords_ore_locked + coords_ore_unlocked)
        print('Number of Ores:', num)
        if num < n:
            return True
        else:
            return False

    def Locked_Ores_Less_Than(self, n):
        coords_ore_locked = self.mb.locate(self.box, './PNG/ore_locked.PNG', self.confidence)
        num = len(coords_ore_locked)
        print('Number of Locked Ores:', num)
        if num < n:
            return True
        else:
            return False

    def Full_Capacity(self):
        coords_100 = self.mb.locate(self.box, './PNG/100.PNG', self.confidence)
        num = len(coords_100)
        print('Capacity Full:', num)
        if num == 1:
            return True
        else:
            return False
    
    def Aquire_Target(self, ores, drags):
        y_drag = -200
        flag = False
        for ore in ores:
            coords_ore = self.mb.locate(self.box, ore, self.confidence)
            if len(coords_ore) >= 1:
                flag = True
            else:
                for i in range(drags):
                    self.mb.drag(self.box, SMALLBOX, 0, y_drag, dur=1, t=1, padding=.95)
                    coords_ore = self.mb.locate(self.box, ore, self.confidence)
                    if len(coords_ore) >= 1:
                        flag = True
                        break
            if flag:
                print('Acquired Target:', ore)
                break
            y_drag = -1*(y_drag)
        self._add_variance(coords_ore[0], -25, 5, 25, 5)
        self.mb.click(self.box, coords_ore[0]) # click ore 1
        return flag
    
    def Approach(self, t_approach):
        coords_approach = self.mb.locate(self.box, './PNG/approach.PNG', self.confidence)
        self._add_variance(coords_approach[0], 0, 10, 100, 10)
        self.mb.click(None, coords_approach[0]) # approach ore 1
        self.Sort(by='distance')
        pause(t_approach, text='Approaching') # wait

    def Mine(self, n): # TODO: scroll up
        print('Begin Mining')
        coords_ore_locked = self.mb.locate(self.box, './PNG/ore_locked.PNG', self.confidence)
        coords_ore_unlocked = self.mb.locate(self.box, './PNG/ore_unlocked.PNG', self.confidence)
        self._add_variance(coords_ore_unlocked[0], 0, 10, 100, 10)
        self.mb.click(None, coords_ore_unlocked[0]) # click ore 1

        coords_lock = self.mb.locate(self.box, './PNG/lock.PNG', self.confidence)
        self._add_variance(coords_lock[0], 0, 10, 100, 10)
        self.mb.click(None, coords_lock[0], t=2) # lock ore 1
        self.mb.click(self.box, ABILITY1)
        self.mb.click(self.box, ABILITY2)
        for i in range(1, n-len(coords_ore_locked)): # for each remaining unlocked; lock
            try:
                self._add_variance(coords_ore_unlocked[i], 0, 10, 100, 10)
                self.mb.click(None, coords_ore_unlocked[i]) # click ore i
                coords_lock = self.mb.locate(self.box, './PNG/lock.PNG', self.confidence)
                self._add_variance(coords_lock[0], 0, 10, 100, 10)
                self.mb.click(None, coords_lock[0]) # lock ore i
            except IndexError:
                print('Lock button not found; skipping.')

    def To_Station(self, shortcut, station, confirm, t_station):
        print('To Station')
        if shortcut is not None:
            self.mb.click(self.box, shortcut, t=2)
        self.mb.click(self.box, PERSONALASSETS, t=5)
        self.mb.click(self.box, station, t=2)
        self._start_autopilot(confirm)
        pause(t_station, text='Autopiloting to Station')

    def Unload_And_Stack_All(self):
        print('Unloading and Stacking All')
        self.mb.click(self.box, X, t=2) # close event
        self.mb.click(self.box, SHORTCUT1, t=2)
        self.mb.click(self.box, OREHOLD, t=2)
        self.mb.click(self.box, SELECTALL, t=2)

        coords_move_to = self.mb.locate(self.box, './PNG/move_to.PNG', self.confidence)
        if len(coords_move_to) == 1:
            self._add_variance(coords_move_to[0], 0, 10, 100, 10)
            self.mb.click(None, coords_move_to[0], t=2)
            self.mb.click(self.box, ITEMHANGER_SMALL, t=2)
        else:
            self.mb.click(self.box, ITEMHANGER_BIG, t=2)

        self.mb.click(self.box, SELECTALL)
        coords_stack_all = self.mb.locate(self.box, './PNG/stack_all.PNG', self.confidence)
        if len(coords_stack_all) == 1:
            self._add_variance(coords_stack_all[0], 0, 10, 100, 10)
            self.mb.click(None, coords_stack_all[0], t=5)
        else:
            self.mb.click(self.box, SELECTALL, t=2)

    def Undock(self, t_undock):
        self.mb.click(self.box, X, t=2) # close event
        print('Undocking')
        self.mb.click(self.box, UNDOCK)
        pause(t_undock, text='Undocking')