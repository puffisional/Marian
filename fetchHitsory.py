# -*- coding: utf-8 -*-

from __future__ import print_function, division
import urllib2
from bs4 import BeautifulSoup
import datetime
import json
import urllib
from keno10Fetcher.connectVars import getPostData
from keno10Fetcher import connectVars
import mysql.connector


def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 

def giveValue(ele):
    return int(ele.string)

def parseKenoUrl(url='https://eklubkeno.etipos.sk/Archive.aspx', data={}):
    data = urllib.urlencode(data)
    query = urllib2.Request(url, data)
#     query.add_header('Content-Type', 'application/x-www-form-urlencoded')
#     query.add_header("Cookie", "ASP.NET_SessionId=j3ugmhm24sqjujyhswescdfy; EBetClientLanguage=sk; __utma=4204135.1467038233.1509125842.1509125842.1509170892.2; __utmb=4204135.35.10.1509170892; __utmc=4204135; __utmz=4204135.1509170892.2.2.utmcsr=tipos.sk|utmccn=(referral)|utmcmd=referral|utmcct=/")
    ff = urllib2.urlopen(query)
    xmlstring = ff.read()
    soup = BeautifulSoup(xmlstring, 'html.parser')
    numbers = soup.findAll("td", {"class":"gameListItem"})
    dates = soup.findAll("option", {"selected":"selected"})

    if len(numbers) == 0:
        try:
            return (soup.find("input", {"id":"__VIEWSTATE"})["value"], 
                   soup.find("input", {"id":"__EVENTVALIDATION"})["value"])
        except TypeError:
            return None
    
    day = int(dates[0]["value"])
    month = int(dates[1]["value"])
    year = int(dates[2]["value"])
    hour = int(dates[3]["value"])      
    numbers = map(giveValue, numbers)    lotteryList = []    
    for i in range(int(len(numbers)/20)):        lotteryList.append(numbers[i*20:i*20+20])
    
    try: 
        tahy = []           for index, tah in enumerate(reversed(lotteryList)):
            tahy.append({                "day": day,                "month": month,                "year": year,                "hour": hour,                "minute": index*5,                "timestamp":totimestamp(datetime.datetime(year, month, day, hour, index*5, 0)),                "numbers": tah                })
    except:
        return None
    
    return tahy

def sync(day, month, year, hour):
    cnx = mysql.connector.connect(user='martin', password='svn78KE!#',
                              host='127.0.0.1',
                              database='keno')
    cursor = cnx.cursor()
    add_tah = ("INSERT INTO pots(datetime, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15, num16, num17, num18, num19, num20) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    
    data = getPostData(day, month, year, hour)
    tahy = parseKenoUrl(data=data)
    if isinstance(tahy, tuple):
        connectVars.viewState, connectVars.eventValidaton = tahy
         
        data = getPostData(day, month, year, hour)
        tahy = parseKenoUrl(data=data)
 
        if isinstance(tahy, tuple): 
            print("skipping", month, day, year, hour)
            return
         
    if tahy is None:
        return   
     
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
    cnx.close()
