import RPi.GPIO as GPIO
import time
import http.client as httplib
import urllib
import datetime

class watertank:
    def __init__(self):
        print("water tank system working")
        TRIG = 2
        ECHO = 4

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, False)

        print ("Waiting For Sensor To Settle")
        time.sleep(1) 

        def get_distance():
            print("getting distance")
            dist_add = 0
            k=0
            for x in range(20):
                try:
                    GPIO.output(TRIG, True)
                    time.sleep(0.00001)
                    GPIO.output(TRIG, False)

                    while GPIO.input(ECHO)==0:
                        print("echo low") 
                        pulse_start = time.time()

                    while GPIO.input(ECHO)==1:
                        pulse_end = time.time()

                    pulse_duration = pulse_end - pulse_start

                    distance = pulse_duration * 17150

                    distance = round(distance, 3)
                    print (x, "distance: ", distance)

                    if(distance > 125):
                        k=k+1
                        continue
        
                    dist_add = dist_add + distance
                    time.sleep(.1)
        
                except Exception as e: 
        
                    pass


            print ("x: ", x+1)
            print ("k: ", k)

            avg_dist=dist_add/(x+1 -k)
            dist=round(avg_dist,3)

            return dist

        self.distance=get_distance()

        print ("distance: ", self.distance)


        
        params = urllib.parse.urlencode({'field1': self.distance, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (response.status, response.reason)
            conn.close()
        except:
            print("error at posting command")

        print ("---------------------")


water = watertank()