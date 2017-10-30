from marian import Marian
import time
import better
from random import randint
import random
import datetime
from math import floor, ceil

def ceil_dt(dt):
    deltaMin = int(ceil(dt.minute / 5.) * 5)
    if deltaMin == 60:
        dt = dt + datetime.timedelta(minutes=60)
        deltaMin = 0
        
    return dt.replace(second=0, microsecond=0, minute=deltaMin)

marian = Marian()
# marian.getRepeatedNumbers("2017-10-28 00:00:00", "2017-10-28 19:00:00")


for i in range(5):
    better.kenoLogin()
    
    now = datetime.datetime.now()
    marian.getRepeatedNumbers(now - datetime.timedelta(minutes=60), now)
    marian.prepareBet(ceil_dt(now))
    
    print(marian.stats)
    time.sleep(300)