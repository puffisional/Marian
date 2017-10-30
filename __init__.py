import mysql.connector

def connectMysql():
    cnx = mysql.connector.connect(user='martin', password='svn78KE!#',
                              host='127.0.0.1',
                              database='keno')
    return cnx