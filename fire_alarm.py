import RPi.GPIO as GPIO
import time
import http.client as httplib
import urllib


class firealarm:
    def __init__(self):
        print("Fire alarm system working")
        key = 'IQ2F3XORLRSR8RY2'
        fire = 2
        buzzer = 4

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fire,GPIO.IN)
        GPIO.setup(buzzer,GPIO.OUT)
        GPIO.output(buzzer,GPIO.LOW)

        try:
            while True:
                reading = GPIO.input(fire)
                if reading:
                    print("fire detected")
                    while True:
                        print("true at gpio 4")
                        GPIO.output(buzzer,GPIO.HIGH)
                        time.sleep(0.25)
                        GPIO.output(buzzer,GPIO.LOW)
                        time.sleep(0.25)
                        if not GPIO.input(fire):
                            break
                else:
                    print("false at fire alarm")
                    GPIO.output(25,GPIO.LOW)
                params = urllib.parse.urlencode({'field1': reading, 'key':key }) 
                headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                conn = httplib.HTTPConnection("api.thingspeak.com:80")
                try:
                    conn.request("POST", "/update", params, headers)
                    response = conn.getresponse()
                    print (response.status, response.reason)
                    conn.close()
                except:
                    print("error at posting command")
                    
                
        finally:
            print("Cleaning Up.....")
            GPIO.cleanup()
            

if __name__ == '__main__':
    smoke = firealarm()
    


