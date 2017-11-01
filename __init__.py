import mysql.connector

STRAT_RANDOM = 0
STRAT_FIXED = 1
STRAT_TIER = 2
STRAT_DISTRIBUTION = 3

TIER_TOP = -1
TIER_AVERGAE = "average"
TIER_LOW = "low"

DEFAULT_TIER_SIZE = 4
DEFAULT_TIER_OFFSET = 60
DEFAULT_TIER = TIER_TOP
DEFAULT_START_OFFSET = 0

DT_HASH = [None]

def connectMysql():
    cnx = mysql.connector.connect(user='martin', password='svn78KE!#',
                              host='127.0.0.1',
                              database='keno')
    return cnx