import threading
from bot import *


params = {'confidence': .78,
          'drags': 5,
          'max_targets': 4,
          'min_ores': 4,
          'min_ores_locked': 1, # keep at 1 or bot may deactivate miner when Locked_Ores_Less_Than is true and Ores_Less_Than is False
          'ores': ['./PNG/Ores/crokite.PNG',
                   './PNG/Ores/jaspet.PNG',
                   './PNG/Ores/bistot.PNG',
                   './PNG/Ores/arkonor.PNG',
                   './PNG/Ores/hemorphite.PNG',
                   './PNG/Ores/hedbergite.PNG'],
          'signal': 'PNG/signals/cluster.PNG',
          't_approach': 120, # ensure it's long enough or mb.locate won't find lock
          't_check': 60,
          't_mine': 20*60,
          't_station2': 60,
          't_station3': 60,
          't_undock': 15,
          't_warp': 30}

bar_top = 50
bar_bottom = 10

size = (960, 540 + bar_top + bar_bottom)
locs = [(0, 0), (0, size[1])]
mb = MultiBox(size, locs)

bot0 = Bot(mb, 0, params)
# bot1 = Bot(mb, 1, params)

t0 = threading.Thread(target=bot0.run, args=(), kwargs={})
# t1 = threading.Thread(target=bot1.run, args=(), kwargs={})

t0.start()
# time.sleep()
# t1.start()