# -*- coding: utf-8 -*-
from __future__ import print_function, division

from marian import Marian as m
from __init__ import connectMysql, STRAT_RANDOM, STRAT_FIXED, STRAT_TIER,\
    DEFAULT_START_OFFSET, DEFAULT_TIER_OFFSET, STRAT_DISTRIBUTION
from Marian import strategies
from Marian.tools import ceilDatetime
import datetime
import Marian

msql = connectMysql()

cursor = msql.cursor()
query = "SELECT datetime from pots where datetime between '2017-08-03 07:55:00' and '2017-08-04 07:55:00'"

marian = m(simulateBets=True)

success = []

cursor.execute(query)
msql.close()

if __name__ == "__main__":
    
    Marian.DT_HASH[0] = hash("2017-08-05 09:00:00"+"smallCheck")
    
    for datetime in cursor:
        marian.prepareBet(datetime[0], STRAT_DISTRIBUTION)
        print(datetime[0], marian.stats)
        
    #     print(marian.stats)     
    #     print( (float(marian.stats["hits"]) / float(marian.stats["bets"])) * 100)
        
    
    # def randomBets():
    
    
    # for tierIndex, tier in enumerate(marian.tiers):
    #     
    #     marian.prefferedTier = tierIndex
    #     cursor.execute(query)
    #     
    #     for datetime in cursor:
    #         marian.prepareBet(datetime[0])
    #     print(marian.stats)     
    #     print( (float(marian.stats["hits"]) / float(marian.stats["bets"])) * 100, marian.prefferedTier, marian.tiers[marian.prefferedTier])
        
    #     marian.stats = stats = {
    #         "bets":0,
    #         "hits":0,
    #         "miss":0,
    #         }
    
