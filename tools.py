import random
from Marian import connectMysql
from math import ceil
import datetime
import operator
import copy
from threading import Thread
from multiprocessing.pool import ThreadPool
import multiprocessing
import inspect

def getRepeatedNumbers(fromDate, toDate, tierSize=4):
        msql = connectMysql()
        cursor = msql.cursor()
        numberDistribution = []
        for i in range(1, 81):
            query = "select count(*) as distribution from pots where (num1=%s or num2=%s or num3=%s or num4=%s or num5=%s or \
                                                     num6=%s or num7=%s or num8=%s or num9=%s or num10=%s or \
                                                     num11=%s or num12=%s or num13=%s or num14=%s or num15=%s or \
                                                     num16=%s or num17=%s or num18=%s or num19=%s or num20=%s) \
                                                     and datetime between %s and %s"
            data = ("%s" % i,) * 20 + (fromDate, toDate)
            cursor.execute(query, data)
            numberDistribution.append((i, cursor.fetchone()[0]))
        
        numberDistribution.sort(key=lambda x: x[1])
        tiers = []
        ranging = int(80 / tierSize)
        for i in range(ranging):
            tier = [i[0] for i in numberDistribution[i * tierSize: i * tierSize + tierSize]]
            tiers.append(tier)
        
        msql.close()
        return tiers
    
def ceilDatetime(dt):
    deltaMin = int(ceil(dt.minute / 5.) * 5)
    if deltaMin == 60:
        dt = dt + datetime.timedelta(minutes=60)
        deltaMin = 0
        
    return dt.replace(second=0, microsecond=0, minute=deltaMin)

def getNumberDistribution(number, fromDate, toDate):
    msql = connectMysql()
    distribution = {
        "hits":[],
        "avgHits":0,
        "misses":[],
        "combined":[],
        "avgMisses":0,
        }
    count = 0
    cursor = msql.cursor()
    trend = None
    
    while fromDate != toDate:
        query = "select * from pots where datetime=%s"
        cursor.execute(query, (fromDate,))

        try:
            numbers = cursor.fetchone()[2:]
            
            if number in numbers:
                if trend is not None and trend == -1:
                    distribution["misses"].append(count)
                    distribution["combined"].append(-count)
                    count = 0
                    
                count += 1
                trend = 1
            else: 
                if trend is not None and trend == 1:
                    distribution["hits"].append(count)
                    distribution["combined"].append(count)
                    count = 0
                
                count += 1
                trend = -1
        except:
            continue
        finally:
            fromDate += datetime.timedelta(minutes=5)
        
    if trend is not None and trend == -1:
        distribution["misses"].append(count)
        distribution["combined"].append(-count)
        count = 0
    if trend is not None and trend == 1:
        distribution["hits"].append(count)
        distribution["combined"].append(count)
        count = 0
        
    distribution["avgHits"] = max(distribution["hits"]) / 2
    distribution["avgMisses"] = max(distribution["misses"]) / 2
    distribution["hitRatio"] = len(distribution["hits"]) / len(distribution["hits"])
    
    msql.close()
    return distribution

def findPatterns(distribution, patternWidth=2):
    patterns = {}
    meta = {
        "hitPatterns": 0,
        "missPatterns": 0,
        }
    try:
        for index, point in enumerate(distribution):
            pattern = distribution[index:index+patternWidth]
            nextTrend = 1 if distribution[index+patternWidth] > 0 else -1
            
            if nextTrend == 1:
                meta["hitPatterns"] += 1
            else:
                meta["missPatterns"] += 1
                 
            pattern.append(nextTrend)
            pattern = tuple(pattern)
            patternCount = patterns.get(pattern, 0)
            if patternCount == 0: patterns[pattern] = 0
             
            patterns[pattern] += 1 
    except IndexError:
        pass
    
    return patterns, meta
        
def getPatternProbability(sortedPatterns, patterns):
    patternProbabilities = {}
    
    for pattern, quantity in sortedPatterns:
        trend = pattern[-1]
        pattern = pattern[:-1]
        
        counterPattern = pattern + (-trend,)
        counterPatternQuantity = patterns.get(counterPattern, 0)
        if counterPatternQuantity == 0:
            probability = 100
        else:
            probability = quantity / counterPatternQuantity
            
        patternProbabilities[pattern] = (probability, trend)
#         print(pattern, probability, trend, quantity)
        
    return patternProbabilities

def buildPatternProbability(fromDate, toDate, patternWidth=2, toPass=3):
    
    manager = multiprocessing.Manager()
    numberPatternProbability = manager.dict()
    
    number = 1
    for _ in range(1):
        jobs = []
        for _ in range(8):
            p = multiprocessing.Process(target=_numberProbability, args=(number, fromDate, toDate, patternWidth, numberPatternProbability, toPass))
            jobs.append(p)
            p.start()
            
            number += 1
             
        for job in jobs:
            job.join()
        
    return numberPatternProbability

def _numberProbability(number, fromDate, toDate, patternWidth=2, target=None, toPass=3):
    # Pass1
    distribution = getNumberDistribution(number, fromDate, toDate)
    
    if toPass == 1:
        if target is None:
            return distribution
        else:
            target[number] = distribution["combined"]
    
    # Pass2
    patterns, meta = findPatterns(distribution["combined"], patternWidth=patternWidth)
    allHits, allMisses, maxHits, maxMisses = sum(distribution["hits"]), sum(distribution["misses"]), \
                                             max(distribution["hits"]), max(distribution["misses"])
                                             
    sortedPatterns = sorted(patterns.items(), key=operator.itemgetter(1))
    
    if toPass == 2:
        if target is None:
            return sortedPatterns
        else:
            target[number] = sortedPatterns
#     maxHitPattern, maxMissPattern = 0,0
#     for (pattern, quantity) in sortedPatterns[-5:]:
#         if pattern[-1] == 1 and quantity > maxHitPattern: maxHitPattern = quantity
#         elif pattern[-1] == -1 and quantity > maxMissPattern: maxMissPattern = quantity
#     for index, pattern in enumerate(sortedPatterns):
#         if pattern[1] == 1: sortedPatterns[index] = (pattern[0], pattern[1], maxHitPattern / pattern[1])
#         elif pattern[1] == -1: sortedPatterns[index] = (pattern[0], pattern[1], maxMissPattern / pattern[1])
#     print(sortedPatterns)
    # Pass 3
    
    
    patternProbabilities = getPatternProbability(copy.deepcopy(sortedPatterns), patterns)
    
    if toPass == 3:  
        if target is None:
            return patternProbabilities
        else:
            target[number] = patternProbabilities, distribution["combined"]

    
