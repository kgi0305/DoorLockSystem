import sqlite3
import threading
import datetime
from twisted.internet import protocol, reactor

conn = sqlite3.connect('Project_DOOR.db', check_same_thread=False)
cur = conn.cursor()


# sql1 = 'CREATE TABLE DOOR_INVADER(C_NUMVER NUMBER(3), YEAR NUMBER(20), RESULT CHAR(20))'
# cur.execute(sql1)

flag_exit = False

def search():
    while True:
        a = input("s는 테이블 불러오기 : ")
        if a == 's':
            print("입력")
            cur.execute('SELECT * FROM DOOR_INVADER')
            print(cur.fetchall())
            conn.commit()
        if flag_exit == True:
            break
        
t1 = threading.Thread(target = search, args=())
t1.start()
cnt=0

transports = set()
pwd = "1234"
input_pass = ""

class Chat(protocol.Protocol):
    def connectionMade(self):
        transports.add(self.transport)


    def dataReceived(self, data):
        global pwd
        global cnt
        print(data)
        
        if data.decode() == '1234':
            now = datetime.datetime.now()
            nowDate1 = now.strftime('%Y-%m-%d %H:%M:%S')
            cnt=cnt+1
            cur.execute("INSERT INTO DOOR_INVADER VALUES (? , ? , 'DOOR_Open')",(cnt,nowDate1,))
            conn.commit()
            for t in transports:
                if self.transport is not t:
                    t.write(b'open')
                    
        elif data.decode() ==  'camera1':
            now = datetime.datetime.now()
            nowDate1 = now.strftime('%Y-%m-%d %H:%M:%S')
            cnt=cnt+1
            cur.execute("INSERT INTO DOOR_INVADER VALUES (? , ? , 'keyCard_worng')",(cnt,nowDate1,))
            conn.commit()
            for t in transports:
                if self.transport is not t:
                    t.write(data)
                    
        elif data.decode() == 'CorrectCard':
            for t in transports:
                if self.transport is not t:
                    t.write(data)
        else:
            now = datetime.datetime.now()
            nowDate1 = now.strftime('%Y-%m-%d %H:%M:%S')
            cnt=cnt+1
            cur.execute("INSERT INTO DOOR_INVADER VALUES (? , ? , 'PassWord_worng')",(cnt,nowDate1,))
            conn.commit()
            for t in transports:
                if self.transport is not t:
                    t.write(b'camera2')
                    

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()



try:
    pass

except KeyboardInterrupt:
    flag_exit = True
    conn.close()
    
finally:
    print("서버 끝")
