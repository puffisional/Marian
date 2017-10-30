# -*- coding: utf-8 -*-
from __future__ import print_function, division
from __init__ import connectMysql

import better
import datetime
import random

class Marian():
    
    lastBetTime = datetime.datetime.now()
    lastBetNumbers = []
    stats = {
        "bets":0,
        "hits":0,
        "miss":0,
        }
    tiers = None
    prefferedTier = -1
    
    def __init__(self):
        self.msql = connectMysql()
    
    def __del__(self):
        self.msql.close()
    
    def bet(self, numbers):
        if len(numbers) == 0: 
            self.lastBetNumbers = []
            return
            
        self.lastBetNumbers = numbers
        self.stats["bets"] += 1
        print(numbers)
        better.betNumbers(numbers)
        
#     def prepareBet(self, nextBetTime):
#         if nextBetTime == self.lastBetTime + datetime.timedelta(minutes=5): 
#             if len(self.lastBetNumbers) > 0:
#                 self.checkBet(self.lastBetTime, self.lastBetNumbers)
#             return
#         
#         cursor = self.msql.cursor()
#         data = (nextBetTime - datetime.timedelta(minutes=5), nextBetTime - datetime.timedelta(minutes=10))
#         cursor.execute("SELECT * from pots where datetime in (%s, %s)", data)
#          
#         index = 0
#         numbers = []
#         for index, date in enumerate(cursor):
#             numbers.append(date[2:])
#         if index == 1:
#             sect = set(numbers[0]).intersection(numbers[1])
#             if len(sect) > 0:
#                 self.bet(self.getFromTier(sect, tier=-1))
#             else:
#                 self.lastBetNumbers = []
#         tier = self.tiers[5]
#         self.bet([tier[randint(0,len(tier)-1)], tier[randint(0,len(tier)-1)]])
        
#         self.lastBetTime = nextBetTime
    
    def prepareBet(self, nextBetTime):
        
#         if nextBetTime == self.lastBetTime + datetime.timedelta(minutes=5): 
#             if len(self.lastBetNumbers) > 0:
#                 self.checkBet(self.lastBetTime, self.lastBetNumbers)
        
        self.bet(self.getRandomFromTier(2, self.prefferedTier))
        self.lastBetTime = nextBetTime
    
    def checkBet(self, betTime, numbers):
        if len(numbers) == 0: return
        
        cursor = self.msql.cursor()
        cursor.execute("SELECT * from pots where datetime=%s", (betTime,))
        pottedNumbers = cursor.fetchone()[2:]
        sect = list(set(pottedNumbers).intersection(numbers))
        
        if len(sect) == 2:
            self.stats["hits"] += 1
        else:
            self.stats["miss"] += 1
            
    def getRepeatedNumbers(self, fromDate, toDate, tierSize=4):
        cursor = self.msql.cursor()
        numberDistribution = []
        for i in range(1, 81):
            query = "select count(*) as distribution from pots where (num1=%s or num2=%s or num3=%s or num4=%s or num5=%s or \
                                                     num6=%s or num7=%s or num8=%s or num9=%s or num10=%s or \
                                                     num11=%s or num12=%s or num13=%s or num14=%s or num15=%s or \
                                                     num16=%s or num17=%s or num18=%s or num19=%s or num20=%s) \
                                                     and datetime between %s and %s"
            data = ("%s" % i,)*20 + (fromDate, toDate)
            cursor.execute(query, data)
            numberDistribution.append((i, cursor.fetchone()[0]))
        
        numberDistribution.sort(key=lambda x: x[1])
        tiers = []
        ranging = int(80/tierSize)
        for i in range(ranging):
            tier = [i[0] for i in numberDistribution[i*tierSize: i*tierSize+tierSize]]
            tiers.append(tier)
        
        self.tiers = tiers
        return tiers
    
    def getFromTier(self, inputNumbers, tier=-1):
        tier = self.tiers[tier]
        sect = set(inputNumbers).intersection(tier)
        return list(sect)
    
    def getRandomFromTier(self, count, tier=-1):
        return random.sample(self.tiers[tier], count)
