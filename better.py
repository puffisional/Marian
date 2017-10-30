# -*- coding: utf-8 -*-

from __future__ import print_function, division
import urllib2
import urllib
from bs4 import BeautifulSoup

login = "puffisan"
password = "mac87cz"
pin = "737164"
cookie = "pcId=PlayerId=143055&CookieId=f83aa400-4283-46aa-8476-25c3c801f732; __utmt=1; ASP.NET_SessionId=wvxdf2q3ogt0ljqp4ihlqeuv; __utma=4204135.1467038233.1509125842.1509225950.1509250322.7; __utmb=4204135.34.10.1509250322; __utmc=4204135; __utmz=4204135.1509250322.7.5.utmcsr=eklubkeno.etipos.sk|utmccn=(referral)|utmcmd=referral|utmcct=/Keno5.aspx; __utmli=ctl00_MiddlePlaceHolder_PlayerLogin_LogOn"

def addHeader(query):
    global cookie
    query.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    query.add_header("Accept",'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
    query.add_header("Accept-Encoding","gzip, deflate, br")
    query.add_header("Connection","keep-alive")
    query.add_header("DNT","1")
    query.add_header("Origin","https://eklubkeno.etipos.sk")
    query.add_header("Referer","https://eklubkeno.etipos.sk/Keno5.aspx")
    query.add_header("Upgrade-Insecure-Requests","1")
    query.add_header("Cookie", cookie)

def kenoLogin():
    global cookie
    url = "https://www.etipos.sk/Player/Login.aspx"
    
    query = urllib2.Request(url)
    addHeader(query)
#     query.add_header("Cookie", cookie)
    ff = urllib2.urlopen(query)
    xmlstring = ff.read()
    soup = BeautifulSoup(xmlstring, 'html.parser')
    
    data = {}
    items = soup.findAll("input")
    for item in items:
        print(item["name"])
        try:
            data[item["name"]] = item["value"]
        except:
            data[item["name"]] = ""
            
    data["ctl00$MiddlePlaceHolder$PlayerLogin$Login"] = login
    data["ctl00$MiddlePlaceHolder$PlayerLogin$Password"] = password
    data["ctl00$MiddlePlaceHolder$PlayerLogin$LogOn"] = "Prihlásiť"
    
    
    query = urllib2.Request(url, urllib.urlencode(data))
    addHeader(query)
    ff = urllib2.urlopen(query)
    xmlstring = ff.read()
    
def betNumbers(numbers):
    url = "https://eklubkeno.etipos.sk/Keno5.aspx"
    
    query = urllib2.Request(url)
    query.add_header("Cookie", cookie)
    ff = urllib2.urlopen(query)
    xmlstring = ff.read()
    soup = BeautifulSoup(xmlstring, 'html.parser')
    viewState, eventValidation, viewGenerator = (soup.find("input", {"id":"__VIEWSTATE"})["value"], 
                                                soup.find("input", {"id":"__EVENTVALIDATION"})["value"],
                                                soup.find("input", {"id":"__VIEWSTATEGENERATOR"})["value"])
    
    data = {
        "__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        "__VIEWSTATE":viewState,
        "__VIEWSTATEGENERATOR":viewGenerator,
        "__EVENTVALIDATION":eventValidation,
        "_ctl0:hdnNumGamesWebBaseUrl":"https://www.etipos.sk",
        "_ctl0:LoginControl:LoggedMinutesID":8,
        "_ctl0:ContentPlaceHolder:hdnStep":1,
        "_ctl0:ContentPlaceHolder:hdnRandomTip":0,
        "_ctl0:ContentPlaceHolder:cmbNumbers":len(numbers),
        "_ctl0:ContentPlaceHolder:cmbBet":"0,30",
        "_ctl0:ContentPlaceHolder:cmbDraws":1,
        "ticket1": "",
        "ticket2": "",
        "_ctl0:ContentPlaceHolder:btnSubmit":"Odoslať",
        }
    
    for number in numbers:
        data["ticket1_%i" % number] = "1_%i" % number
    
    query = urllib2.Request(url, urllib.urlencode(data))
    addHeader(query)
    ff = urllib2.urlopen(query)
    xmlstring = ff.read()
    
    soup = BeautifulSoup(xmlstring, 'html.parser')
    items = soup.findAll("input")
    data = {}
    for item in items[:9]:
        data[item["name"]] = item["value"]
    
    data["_ctl0:ContentPlaceHolder:btnSubmit"] = "Odoslať"
    
    query = urllib2.Request(url, urllib.urlencode(data))
    addHeader(query)
    
    ff = urllib2.urlopen(query)
    payUrl = ff.geturl()
    xmlstring = ff.read()
    
    soup = BeautifulSoup(xmlstring, 'html.parser')
    items = soup.findAll("input")
    data = {}
    for item in items:
        try:
            data[item["name"]] = item["value"]
        except:
            data[item["name"]] = ""
    
    pinQuestion = soup.find("label", {"for":"ctl00_MiddlePlaceHolder_ctlBetPayment_PinNumbers"}).text
    a,b = int(pinQuestion[0])-1, int(pinQuestion[5])-1
    
    data["ctl00$MiddlePlaceHolder$ctlBetPayment$Login"] = login
    data["ctl00$MiddlePlaceHolder$ctlBetPayment$Password"] = password
    data["ctl00$MiddlePlaceHolder$ctlBetPayment$PinNumbers"] = "%s%s" % (pin[a], pin[b])
    data["ctl00$MiddlePlaceHolder$ctlBetPayment$Send"] = "Odoslať"

    query = urllib2.Request(payUrl, urllib.urlencode(data))
    
    query.add_header("Cookie", cookie)
    addHeader(query)
    
    ff = urllib2.urlopen(query)
    xmlstring = ff.read()