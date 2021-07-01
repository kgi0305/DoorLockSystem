#camera2는 패스워드가 틀림
#camera1은 rfid가 틀림 
import socket
import select
import sys
import RPi.GPIO as GPIO
from pirc522 import RFID
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('220.69.249.245', 8000))
print(s)

cnt_pas=0
cnt_rfid=0
row_val = [0,0,0,0]
num_bak = [[1,2,3,4],
           [5,6,7,8],
           [9,'a','b','c'],
           ['e','f','g','h']]
RFID_UID = [76, 248, 158, 22, 60]
rc522 = RFID()

# setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# pin config
               #  C1,C2,C3,C4
KEYPAD_COL_PIN = [40,38,37,36]
               #  R1,R2,R3,R4
KEYPAD_ROW_PIN = [29,31,33,35]
servo_pin = 11

# pinMode
for i in range(len(KEYPAD_ROW_PIN)):
    GPIO.setup(KEYPAD_ROW_PIN[i], GPIO.OUT, initial=False)
for i in range(len(KEYPAD_COL_PIN)):
    GPIO.setup(KEYPAD_COL_PIN[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo_pin , GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)


# serialP = serial.Serial("/dev/ttyS0",baudrate=115200 , timeout = 3.0)


# #비밀번호 검사함수
# def passward_check(check_pass,set_pass):
#     global cnt_pas
#     if len(check_pass)==4:
#         if check_pass ==set_pass:
#             print("정답/문열림")
#             s.send(f'open'.encode())
#         else:
#             print("비밀번호 틀림")
#             s.send(f'camera2'.encode()) #부저 


#비밀번호 입력 함수
def passward_input():
    user_paswd = ""
    pre = 0
    flag = 0
    while len(user_paswd) < 4:
                    for i in range(len(KEYPAD_ROW_PIN)):
                        GPIO.output(KEYPAD_ROW_PIN[i], True)
                        num1=i
                        for j in range(len(KEYPAD_COL_PIN)):
                            num2=j
                            btn_val = GPIO.input(KEYPAD_COL_PIN[j])
                            if btn_val == 1:
                                    user_paswd+=str(num_bak[num1][num2])
                                    print(user_paswd)
                        GPIO.output(KEYPAD_ROW_PIN[i], False)
                        time.sleep(0.05)
                        
                    #pre = btn_val
                    
    s.send(user_paswd.encode())

try:                        
    while True:
        rc522.wait_for_tag()
        (error, tag_type) = rc522.request()
        if not error : 
            (error, uid) = rc522.anticoll()
            if not error : 
                if RFID_UID == uid :
                    print("키카드 확인/비밀번호 입력하시오.")
                    print(format(uid))
                    s.send(f'CorrectCard'.encode()) 
                    passward_input()
                    print("비밀번호 입력 완료")
                    
    #               serialP.write(bytes(format(uid)+"accept",encoding="utf-8"))
                else :
                    print("키카드 틀림")
                    s.send(f'camera1'.encode()) # 소리 울림 

                time.sleep(1)
            
finally:
    GPIO.cleanup()

# while True:
#     read, write, fail = select.select((s,sys.stdin), (), ())
# 
# 
#     for desc in read:
#         if desc == s:
#             data = s.recv(4096)
#             print(data.decode())
#         else:
#             msg = desc.readline()
#             msg = msg.replace('\n', '')
#             s.send(msg.encode())
