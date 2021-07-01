import sqlite3
import threading
import datetime
from twisted.internet import protocol, reactor

conn = sqlite3.connect('Project_DOOR.db')
cur = conn.cursor()

now = datetime.datetime.now()
nowDate1 = now.strftime('%Y%m%d')
#sql1 = 'DROP TABLE DOOR_INVADER'
sql1 = 'CREATE TABLE DOOR_INVADER(C_NUMBER integer, YEAR text, RESULT text)'
cur.execute(sql1)

conn.commit()
conn.close()