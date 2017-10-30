# -*- coding: utf-8 -*-
from __future__ import print_function, division

from marian import Marian
from __init__ import connectMysql
import datetime
import pyqtgraph as pg
import numpy as np
from PyQt4.Qt import QApplication
import sys

app = QApplication(sys.argv)
msql = connectMysql()

marian = Marian()

def getRepeatedNumbers(fromDate, toDate, tierSize=4):
        cursor = msql.cursor()
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
        return numberDistribution

def getNumberDistribution(number, fromDate, toDate):
    distribution = []
    count = 0
    cursor = msql.cursor()
    
    while fromDate != toDate:
        query = "select * from pots where datetime=%s"
        cursor.execute(query, (fromDate,))
        if fromDate.minute == 0: count = -count
        try:
            numbers = cursor.fetchone()[2:]
        
            if number in numbers: count += 1
            else: count -= 1
            
            distribution.append(count)
        except:
            continue
        finally:
            fromDate += datetime.timedelta(minutes=5)
        
    return distribution

plotWidget = pg.plot(title="Three plot curves")

# for hour in range(6,7):
#     rates = getRepeatedNumbers("2017-10-29 %i:00:00" % hour, "2017-10-29 %i:55:00" % hour, tierSize=80)
#     plotWidget.plot([i[0] for i in rates], [i[1] for i in rates])

# rates = marian.getRepeatedNumbers("2017-10-26 05:00:00", "2017-10-27 23:55:00", tierSize=80)
# plotWidget.plot(range(0,80), rates[0])

fromDate = datetime.datetime.strptime('2017-09-01 05:00:00', '%Y-%m-%d %H:%M:%S')
toDate = datetime.datetime.strptime('2017-10-28 09:00:00', '%Y-%m-%d %H:%M:%S')
oneDistribution = getNumberDistribution(80, fromDate, toDate)
plotWidget.plot(range(len(oneDistribution)), oneDistribution)

msql.close()



# for i in range(3):
#     plotWidget.plot(x, y[i], pen=(i,3))
    
app.exec_()