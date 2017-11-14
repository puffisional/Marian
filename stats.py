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
from math import ceil

marian = Maros(simulateBets=True)

fromDate = datetime.datetime.strptime('2017-05-01 08:55:00', '%Y-%m-%d %H:%M:%S')
toDate = datetime.datetime.strptime('2017-08-05 09:05:00', '%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    
    numProb = _numberProbability(1, fromDate, toDate, 1, None, 1)
    a,b = np.histogram(numProb["hits"], bins=max(numProb["hits"]))
    print(a, map(ceil, b))
#     
    a,b = np.histogram(numProb["misses"], bins=max(numProb["misses"]))
    print(a, map(ceil, b))