# -*- coding: utf-8 -*-
from __future__ import print_function, division
from __init__ import connectMysql

import better
import datetime
import random
from Marian.strategies import getStrategy, STRAT_RANDOM, STRAT_FIXED, STRAT_TIER, STRAT_DISTRIBUTION

class Marian():
    
    def __init__(self, simulateBets=False):
        self.msql = connectMysql()
        self.simulationMode = simulateBets
        self.stats = {
        "bets":0,
        "hits":0,
        "miss":0,
        }
        self.lastBetTime = datetime.datetime.now()
        self.lastBetNumbers = []
        self.prefferedTier = -1
        self.betNumbersCount = 2
        self.fixedStratNumbers = [1, 80]
    
    def __del__(self):
        self.msql.close()
    
    def bet(self, numbers):
        if len(numbers) == 0: 
            self.lastBetNumbers = []
            return
        
        self.lastBetNumbers = numbers
        self.stats["bets"] += 1
        
        if not self.simulationMode:
            better.betNumbers(numbers)
        
    def prepareBet(self, nextBetTime, strategyId=STRAT_RANDOM):
        
        if nextBetTime == self.lastBetTime + datetime.timedelta(minutes=5): 
            if len(self.lastBetNumbers) > 0:
                self.checkBet(self.lastBetTime, self.lastBetNumbers)
        
        strategy = getStrategy(strategyId)
        numbers = []
        
        if strategyId == STRAT_RANDOM:
            numbers = strategy(self.betNumbersCount)
        elif strategyId == STRAT_FIXED:
            numbers = strategy(self.fixedStratNumbers)
        elif strategyId == STRAT_TIER:
            numbers = strategy(self.betNumbersCount, toDate = nextBetTime - datetime.timedelta(minutes=30), tierSize=3, tier=-2)
        elif strategyId == STRAT_DISTRIBUTION:
            numbers = strategy(self.betNumbersCount, nextBetTime)
            print(numbers)
            
        self.bet(numbers)
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
        
        self.stats["lastBettime"] = betTime
         
    def applyStrategy(self, strategyId):
        pass
    
    def checkLastBet(self):
        self.checkBet(self.lastBetTime, self.lastBetNumbers)
