import mysql.connector

def connectMysql():
    cnx = mysql.connector.connect(user='martin', password='ruPP2.GO!#',
                              host='127.0.0.1',
                              database='keno')
    return cnx