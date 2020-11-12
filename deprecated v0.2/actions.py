from coords import *
from multibox import *


bar_top = 50
bar_bottom = 10

size = (960, 540 + bar_top + bar_bottom)
locs = [(0, 0), (0, size[1])]
mb = MultiBox(size, locs)

def add_variance(coords, x1, y1, x2, y2):
    coords[0] -= x1 # adds width variance
    coords[1] -= y1 # adds height variance
    coords[2] += x2 # adds width variance
    coords[3] += y2 # adds height variance

def start_autopilot(confirm, box=0):
    print('Start Auto Pilot')
    mb.click(JUMP, box=box) # click jump
    mb.click(SETASDESTINATION, box=box) # set as destination
    mb.click(ABILITY1, box=box) # close map
    mb.click(X, box=box) # click X
    mb.click(STARTAUTOPILOT, box=box) # begin autopilot
    if confirm:
        mb.click(CONFIRM, box=box) # confirm if in station

def Click_Eye(box=0):
    print('Clicking Eye')
    mb.click(EYE, box=box)

def To_Random_Signal(t_warp, confidence=.78, box=0):
    print('To Random Signal')
    mb.click(DROPDOWN, box=box) # click dropdown menu
    mb.click(DROPDOWN1, box=box)  # filter by signal

    coords_signal = mb.locate('./PNG/asteroid.PNG', confidence, box)
    i = random.randint(1, len(coords_signal)-1)
    add_variance(coords_signal[i], 0, 10, 100, 10)
    mb.click(coords_signal[i]) # click random signal (2:N)

    coords_warp = mb.locate('./PNG/warp.PNG', confidence, box)
    add_variance(coords_warp[0], 0, 10, 100, 10)
    mb.click(coords_warp[0]) # warp
    
    pause(t_warp, text='Warping') # wait
    
def Ores_Less_Than(n, confidence=.78, box=0):
    mb.click(DROPDOWN, box=box) # click dropdown menu
    mb.click(DROPDOWN2, box=box) # filter by asteroid
    coords_ore_unlocked = mb.locate('./PNG/ore_unlocked.PNG', confidence, box)
    coords_ore_locked = mb.locate('./PNG/ore_locked.PNG', confidence, box)
    num = len(coords_ore_locked + coords_ore_unlocked)
    print('Number of Ores:', num)
    if num < n:
        return True
    else:
        return False

def Locked_Ores_Less_Than(n, confidence=.78, box=0):
    coords_ore_locked = mb.locate('./PNG/ore_locked.PNG', confidence, box)
    num = len(coords_ore_locked)
    print('Number of Locked Ores:', num)
    if num < n:
        return True
    else:
        return False

def Full_Capacity(confidence=.78, box=0):
    coords_100 = mb.locate('./PNG/100.PNG', confidence, box)
    num = len(coords_100)
    print('Capacity Full:', num)
    if num == 1:
        return True
    else:
        return False
    
def Approach(t_approach, confidence=.78, box=0): # TODO: if no desired, continue; else, scroll; approach desired;
#     mb.click(DROPDOWN, box=box) # click dropdown menu
#     mb.click(DROPDOWN2, box=box) # filter by asteroid
    mb.click(ITEM1, box=box) # click ore 1
    coords_approach = mb.locate('./PNG/approach.PNG', confidence, box)
    add_variance(coords_approach[0], 0, 10, 100, 10)
    mb.click(coords_approach[0]) # approach ore 1
    pause(t_approach, text='Approaching') # wait

def Mine(n, confidence=.78, box=0): # TODO: scroll up
    print('Begin Mining')
#     mb.click(ITEM1, box=box) # click ore 1
    coords_ore_locked = mb.locate('./PNG/ore_locked.PNG', confidence, box)
    coords_ore_unlocked = mb.locate('./PNG/ore_unlocked.PNG', confidence, box)
    add_variance(coords_ore_unlocked[0], 0, 10, 100, 10)
    mb.click(coords_ore_unlocked[0], t=2) # lock ore 1
    
    coords_lock = mb.locate('./PNG/lock.PNG', confidence, box)
    add_variance(coords_lock[0], 0, 10, 100, 10)
    mb.click(coords_lock[0], t=2) # lock ore 
#     coords_miner = mb.locate('./PNG/miner.PNG', confidence, box)
#     for miner in coords_miner:
#         mb.click(miner, box=box) # activate miner i
    mb.click(ABILITY1, box=box)
    mb.click(ABILITY2, box=box)
    for i in range(1, n-len(coords_ore_locked)): # for each unlocked; lock
        try:
            add_variance(coords_ore_unlocked[i], 0, 10, 100, 10)
            mb.click(coords_ore_unlocked[i], box=box) # click ore i
            coords_lock = mb.locate('./PNG/lock.PNG', confidence, box)
            add_variance(coords_lock[0], 0, 10, 100, 10)
            mb.click(coords_lock[0]) # lock ore i
        except IndexError:
            print('Lock button not found; skipping.')
    
def To_Station(station, shortcut, confirm, t_warp, box=0):
    print('To Station')
    if shortcut is not None:
        mb.click(shortcut, t=2, box=box)
    mb.click(PERSONALASSETS, t=5, box=box)
    mb.click(station, box=box)
    start_autopilot(confirm, box=box)
    pause(t_warp, text='Autopiloting to Station')
    
def Unload_And_Stack_All(confidence, box=0):
    print('Unloading and Stacking All')
    mb.click(X, box=box) # close event
    mb.click(SHORTCUT1, t=2, box=box)
    mb.click(OREHOLD, box=box)
    mb.click(SELECTALL, box=box) 
    
    coords_move_to = mb.locate('./PNG/move_to.PNG', confidence, box)
    if len(coords_move_to) == 1:
        add_variance(coords_move_to[0], 0, 10, 100, 10)
        mb.click(coords_move_to[0], box=box)
        mb.click(ITEMHANGER_SMALL, t=2, box=box)
    else:
        mb.click(ITEMHANGER_BIG, t=2, box=box)
    
    mb.click(SELECTALL, box=box)
    coords_stack_all = mb.locate('./PNG/stack_all.PNG', confidence, box)
    if len(coords_stack_all) == 1:
        add_variance(coords_stack_all[0], 0, 10, 100, 10)
        mb.click(coords_stack_all[0], t=5, box=box)
    else:
        mb.click(SELECTALL, box=box)
    
def Undock(t_undock, box=0):
    print('Undocking')
    mb.click(UNDOCK, box=box)
    pause(t_undock, text='Undocking')