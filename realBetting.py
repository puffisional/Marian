from marian import Marian
import time
import better
from random import randint
import random
import datetime
from math import floor, ceil
from tools import ceilDatetime
from Marian.strategies import STRAT_TIER

marian = Marian()

for i in range(3):
    better.kenoLogin()
    
    now = datetime.datetime.now()
    marian.prepareBet(ceilDatetime(now), strategyId=STRAT_TIER)
    
    time.sleep(300)