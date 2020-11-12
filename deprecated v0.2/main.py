import threading
from bot import *


params = {'confidence': .78,
          'max_targets': 4,
          'min_ores': 4,
          'min_ores_locked': 1, # keep at 1 or bot may deactivate miner when Locked_Ores_Less_Than is true and Ores_Less_Than is False
          't_approach': 60, # ensure it's long enough or mb.locate won't find lock
          't_check': 60,
          't_mine': 25*60,
          't_station2': 150,
          't_station3': 150,
          't_undock': 15,
          't_warp': 30}

bot0 = Bot(0, params)
bot1 = Bot(1, params)

t1 = threading.Thread(target=bot0.run, args=(), kwargs={})
t2 = threading.Thread(target=bot1.run, args=(), kwargs={})

t1.start()
# time.sleep()
# t2.start()https:/go.microsoft.com/fwlink/?LinkID=135170.