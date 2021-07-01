import socket
import select
import sys
import RPi.GPIO as GPIO
import time
import threading
from picamera import PiCamera
import datetime
import drivers
import smbus


flag_exit = False 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('220.69.249.245', 8000))

data =''
str_data=''
distance=0
def read_data_main():
    while True:
        global str_data
        read, write, fail = select.select((s, sys.stdin), (), ())

        for desc in read:
            if desc == s:
                data = s.recv(4096)
                str_data=data.decode()
                print(data.decode())

            else:
                msg = desc.readline()
                msg = msg.replace('\n', '')
                s.send(msg.encode())
                
        if flag_exit ==True:
            break
            
read_data = threading.Thread(target=read_data_main)
read_data.start()
            
GPIO.setmode(GPIO.BCM)

# pin config
servo_pin = 18
trig = 13
echo = 19

GPIO.setup(servo_pin, GPIO.OUT) # pinMode
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

servo_pwm = GPIO.PWM(servo_pin, 50)
servo_pwm.start(2.5) # 0도 설정


display = drivers.Lcd()

# global var

# user function
def wave_main():
     while True :
      global distance
      GPIO.output(trig, False)
      time.sleep(0.5)
      
      GPIO.output(trig, True)
      time.sleep(0.00001)
      GPIO.output(trig, False)
      
      while GPIO.input(echo) == 0 :
        pulse_start = time.time()
      while GPIO.input(echo) == 1 :
        pulse_end = time.time()
      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17000
      distance = round(distance, 2)
      #print("Distance : ", distance, "cm")
      
      if flag_exit ==True:
            break
      
wave = threading.Thread(target=wave_main)
wave.start()
    

def servo_angle(servo, degree):
    # servo_pwm.ChangeDutyCycle(map(degree, 0, 180, 2.5, 12.5))
    # 0도 2.5 90도 7.5 5 180도 12.5 10
    if degree==0:
        servo.ChangeDutyCycle(2.5)
        return
    servo.ChangeDutyCycle(2.5 + degree/180 *10)
    return

def capture():
            print("a")
            camera = PiCamera()
            now = datetime.datetime.now()
            filename = now.strftime('%Y-%m-%d %H:%M:%S')                                                                                                                                                                                                                                 
            camera.start_preview()
            camera.capture('/home/pi/Capture/' + filename + '.jpg')
            print("capture")     
            camera.stop_preview()
            camera.close()
    
try:
    display.lcd_display_string(" Put your card",1)
    display.lcd_display_string(" on the reader",2)
    servo_angle(servo_pwm, 90) 
    while True:
        if str_data != "":
            display.lcd_clear()
            break
    while True:
                if distance <7.5 :
                    time.sleep(1)
                    servo_angle(servo_pwm, 90)

                    print(str_data)
                    time.sleep(0.5)
                    
                
                if str_data == "open":
                    display.lcd_clear()
                    display.lcd_display_string("Open", 1)   # 첫번째 줄에 텍스트 표시                                                                                    
                    servo_angle(servo_pwm, 0)
                    time.sleep(0.5)
                    print("gotocapture")
                    capture()
                    print("end")
                    time.sleep(5)
                    
                                                    
                    
                elif str_data == "camera1":
                    display.lcd_clear()
                    display.lcd_display_string("Wrong card", 1)   # 첫번째 줄에 텍스트 표시     
                    capture()
                    
                elif str_data == "CorrectCard":
                    display.lcd_clear()
                    display.lcd_display_string("Correct card", 1)   # 첫번째 줄에 텍스트 표시     

                elif str_data == "camera2":
                    display.lcd_clear()
                    display.lcd_display_string("Wrong password", 1)   # 첫번째 줄에 텍스트 표시     
                    capture()

                str_data = ''

except KeyboardInterrupt:
    servo_angle(servo_pwm, 0)
    time.sleep(0.5)
    GPIO.cleanup()
    flag_exit =True
    
finally:
    display.lcd_clear()
    read_data.join()
    print("finally")
    
            
            

