from coords import *
from helper import *

    
def start_autopilot(confirm):
    rclick(JUMP)
    rclick(SETASDESTINATION)
    rclick(ABILITY1) # close map
    rclick(X)
    rclick(STARTAUTOPILOT)
    if confirm:
        rclick(CONFIRM)

    
def Mine(t_approach, t_mine):
    rclick(DROPDOWN)
    rclick(DROPDOWN1) # filter asteroid
    rclick(ITEM1, subitem_n=1) # approach ore 1
    wait(t_approach, 'Approaching')
    
    rclick(ITEM1, subitem_n=0) # lock ore 1
    rclick(ABILITY1) # miner 1
    rclick(ABILITY2) # miner 2
    for item in [ITEM2, ITEM3, ITEM4]:
        rclick(item, subitem_n=0) # lock ore i
    wait(t_mine, 'Mining')

    
def To_Asteroid(click_eye, t):
    if click_eye:
        rclick(EYE)
    rclick(DROPDOWN)
    rclick(DROPDOWN3) # filter signal
    if random.random() < .5:
        rclick(ITEM2, subitem_n=1) # warp
    else:
        rclick(ITEM3, subitem_n=1) # warp
    wait(t, 'Warping')
    
 
def To_Station(station, t):
    rclick(SHORTCUT1)
    rclick(PERSONALASSETS)
    rclick(station)
    start_autopilot(confirm=False)
    wait(t, 'Autopiloting to Station')

    
def Unload_Then_To_Station(station, t):
    print('Unloading')
    rclick(X) # close event
    rclick(SHORTCUT1)
    rclick(OREHOLD)
    rclick(SELECTALL) 
    rclick(MOVETO)
    rclick(ITEMHANGER)

    rclick(PERSONALASSETS)
    rclick(station)
    start_autopilot(confirm=True)
    wait(t, 'Autopiloting to Station')

    
def Undock(t):
    rclick(UNDOCK)
    wait(t, 'Undocking')