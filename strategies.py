# -*- coding: utf-8 -*-
from __future__ import print_function, division
import random
import datetime
from Marian.tools import getRepeatedNumbers, buildPatternProbability
from math import floor
from tools import ceilDatetime
import pickle
import os
from Marian import DEFAULT_START_OFFSET, DEFAULT_TIER, DEFAULT_TIER_OFFSET,\
    DEFAULT_TIER_SIZE, TIER_AVERGAE, TIER_LOW, STRAT_RANDOM,\
    STRAT_FIXED, STRAT_TIER, STRAT_DISTRIBUTION
import Marian
import time

def randomNumbers(numbersCount, numbersRange=range(1,80)):
    return random.sample(numbersRange, numbersCount)

def fixedNumbers(numbers):
    return numbers

tierBuffer = {}
def tierNumbers(numbersCount, tier=DEFAULT_TIER, toDate=datetime.datetime.now(), 
                startOffet=DEFAULT_START_OFFSET, offset=DEFAULT_TIER_OFFSET, tierSize=DEFAULT_TIER_SIZE):
    toDate = toDate - datetime.timedelta(minutes=startOffet)
    fromDate = toDate - datetime.timedelta(minutes=offset)
    tierIndex = hash("%s%s" % (fromDate, toDate))
    if tierIndex in tierBuffer:
        tiers =  tierBuffer[tierIndex]
    else:
        tiers = getRepeatedNumbers(fromDate, toDate, tierSize)
        tierBuffer[tierIndex] = tiers

    if tier == TIER_AVERGAE: tier = floor(len(tiers) / 2.)
    elif tier == TIER_LOW: tier = 0
    return random.sample(tiers[tier], numbersCount)


pickleBuffer = "./probabilityBuffer.data"
if os.path.isfile(pickleBuffer):
    with open(pickleBuffer, 'r') as f:
        probabilityBuffer = pickle.load(f)
else:
    probabilityBuffer = None

def probabilityDistNumbers(numbersCount, toDate=datetime.datetime.now(), patternWidth=2):
    global probabilityBuffer, pickleBuffer
    toDate -= datetime.timedelta(minutes=5)
    fromDate = toDate - datetime.timedelta(days=1)
    dateHash = Marian.DT_HASH[0]
    
    if probabilityBuffer is None or dateHash not in probabilityBuffer:
        print(fromDate, toDate)
        buildedProbability = buildPatternProbability(fromDate, toDate, patternWidth)
        
        if probabilityBuffer is None: probabilityBuffer = {}
        probabilityBuffer[dateHash] = buildedProbability.copy()
        
        with open(pickleBuffer, 'w') as f:
            pickle.dump(probabilityBuffer, f)
        
    buildedProbability = probabilityBuffer[dateHash]
    
    fromDate = toDate - datetime.timedelta(days=1)
    shortBuffer = buildPatternProbability(toDate - datetime.timedelta(hours=10), toDate, patternWidth, toPass=1)
    
    numbers = []
    for number, values in buildedProbability.items():
        numberPatternDistribution, pattern = values
        currentPattern = tuple(shortBuffer[number][-patternWidth:])
        print(currentPattern, numberPatternDistribution.get(currentPattern, (100, -1)))
        numberProbability, trend = numberPatternDistribution.get(currentPattern, (100, -1))
        
        if trend == 1:
#             if numberProbability >= 20 and numberProbability < 100:
            if numberProbability == 100:
                print(number, numberPatternDistribution)
                numbers.append(number)
    
    if numbersCount != len(numbers): return []
    
    print(numbers)
    return random.sample(numbers, numbersCount)
    
def getStrategy(strategyId):
    if strategyId == STRAT_RANDOM:
        return randomNumbers
    elif strategyId == STRAT_FIXED:
        return fixedNumbers
    elif strategyId == STRAT_TIER:
        return tierNumbers
    elif strategyId == STRAT_DISTRIBUTION:
        return probabilityDistNumbers