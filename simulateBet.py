# -*- coding: utf-8 -*-
from __future__ import print_function, division

from marian import Marian
from __init__ import connectMysql

msql = connectMysql()

marian = Marian()

marian.getRepeatedNumbers('2017-10-29 11:05:00', '2017-10-29 12:00:00')

cursor = msql.cursor()
query = "SELECT datetime from pots where datetime between '2017-10-29 11:05:00' and '2017-10-29 11:40:00'"



for tierIndex, tier in enumerate(marian.tiers):
    
    marian.prefferedTier = tierIndex
    cursor.execute(query)
    
    for datetime in cursor:
        marian.prepareBet(datetime[0])
    print(marian.stats)     
    print( (float(marian.stats["hits"]) / float(marian.stats["bets"])) * 100, marian.prefferedTier, marian.tiers[marian.prefferedTier])
    
    marian.stats = stats = {
        "bets":0,
        "hits":0,
        "miss":0,
        }
