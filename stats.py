# -*- coding: utf-8 -*-
from __future__ import print_function, division

from marian import Marian
import datetime
import pyqtgraph as pg
import numpy as np
from PyQt4.Qt import QApplication
import sys
import operator
import copy
from tools import buildPatternProbability, ceilDatetime
from Marian.tools import _numberProbability, getNumberDistribution, findPatterns,\
    getPatternProbability
import multiprocessing
from strategies import probabilityDistNumbers, STRAT_DISTRIBUTION
from datetime import timedelta
from Marian.marian import Marian as Maros
import Marian
from Marian.strategies import probabilityBuffer

# app = QApplication(sys.argv)
# msql = connectMysql()
# 
marian = Maros(simulateBets=True)

# plotWidget = pg.plot(title="Three plot curves")
#'2017-08-04 09:00:00' and '2017-08-05 09:05:00'
fromDate = datetime.datetime.strptime('2017-08-04 08:55:00', '%Y-%m-%d %H:%M:%S')
toDate = datetime.datetime.strptime('2017-08-05 09:05:00', '%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
#     patternProbability = buildPatternProbability(fromDate, toDate)
#     print(patternProbability)
#     numberPatternProbability = buildPatternProbability(fromDate, toDate)
            
#     print(numberPatternProbability)
#     probs = probabilityDistNumbers(2, toDate)
#     marian.prepareBet(ceilDatetime(fromDate), STRAT_DISTRIBUTION)
#     marian.checkLastBet()
#     print(marian.stats)
#     marian.prepareBet(ceilDatetime(fromDate) + datetime.timedelta(minutes=5), STRAT_DISTRIBUTION)
#     marian.checkLastBet()
#     print(marian.stats)
    
    Marian.DT_HASH[0] = hash("2017-08-05 09:00:00"+"smallCheck")
    cislo1 = probabilityBuffer[Marian.DT_HASH[0]][3]
    
#     print(cislo1)
#     
#     buildedProbability = probabilityBuffer[Marian.DT_HASH[0]]
#     for number, values in buildedProbability.items():
#         numberPatternDistribution, pattern = values
    
    distribution = getNumberDistribution(7, fromDate, toDate)
    print(distribution["combined"])
     
    patterns, meta = findPatterns(distribution["combined"], patternWidth=2)
    sortedPatterns = sorted(patterns.items(), key=operator.itemgetter(1))
    print(sortedPatterns)
    patternProbabilities = getPatternProbability(copy.deepcopy(sortedPatterns), patterns)
    print(patternProbabilities)
    
#     print(getNumberDistribution(1, fromDate + timedelta(minutes=5), toDate + timedelta(minutes=5))["combined"])
#     print(getNumberDistribution(1, fromDate + timedelta(minutes=10), toDate + timedelta(minutes=10))["combined"])
    
# plotWidget.plot(range(len(distribution["combined"])), distribution["combined"])




# msql.close()



# app.exec_()