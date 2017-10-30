from fetchHitsory import parseKenoUrl
from connectVars import getPostData

import mysql.connector
import connectVars

cnx = mysql.connector.connect(user='martin', password='svn78KE!#',
                              host='127.0.0.1',
                              database='keno')
cursor = cnx.cursor()

years = range(2013, 2014)
months = range(1, 13)
days = range(1, 31)
hours = range(4, 24)

add_tah = ("INSERT INTO pots(datetime, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15, num16, num17, num18, num19, num20) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

# years = range(2014, 2015)
# months = range(4,13)
# days = range(1, 32)
# hours = range(5, 24)

for year in years:
    for month in months:
        for day in days:
            for hour in hours:
                data = getPostData(day, month, year, hour)
                tahy = parseKenoUrl(data=data)
                if isinstance(tahy, tuple):
                    connectVars.viewState, connectVars.eventValidaton = tahy
                    
                    data = getPostData(day, month, year, hour)
                    tahy = parseKenoUrl(data=data)

                    if isinstance(tahy, tuple): 
                        print("skipping", month, day, year, hour)
                        continue
                    
                if tahy is None:
                    continue   
                
                print(tahy)
                
                for tah in tahy:
                    data = [
                        "%s-%s-%s %s:%s:00" % (tah["year"], tah["month"], tah["day"], tah["hour"], tah["minute"]),
                        ]
                    for num in tah["numbers"]:
                        data.append(num)
                    try:
                        cursor.execute(add_tah, tuple(data))
                    except Exception, e:
                        print(e)
                   
                cnx.commit()

# year = 2010
# month = 2
# add_tah = ("INSERT INTO pots(datetime, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15, num16, num17, num18, num19, num20) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
#          
# for day in days:
#     for hour in hours:
#         data = getPostData(day, month, year, hour)
#         tahy = parseKenoUrl(data=data)
#         print(day, month, year, hour)
#         if tahy is None: continue
#           
#         print(tahy)
#           
#         for tah in tahy:
#             data = [
#                 "%s-%s-%s %s:%s:00" % (tah["year"], tah["month"], tah["day"], tah["hour"], tah["minute"]),
#                 ]
#             for num in tah["numbers"]:
#                 data.append(num)
#             try:
#                 cursor.execute(add_tah, tuple(data))
#             except Exception, e:
#                 print(e)
#           
#         cnx.commit()

# data = getPostData(1, 1, 2012, 16)
# tahy = parseKenoUrl(data=data)
# print(tahy)

cnx.close()
