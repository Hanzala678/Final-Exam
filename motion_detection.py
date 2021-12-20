import RPi.GPIO as GPIO
import time
import http.client as httplib
import urllib

GPIO.setwarnings(False)
led = 25
pir = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(led, GPIO.OUT)
key = 'N83794ZZWFS8K7AT'

while True:
    i=GPIO.input(pir)
    if i==0:                 #When output from motion sensor is LOW
        print("No intruders",i)
        GPIO.output(led, 0)  #Turn OFF LED
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print("Intruder detected",i)
        GPIO.output(led, 1)  #Turn ON LED
        time.sleep(0.1)

    params = urllib.parse.urlencode({'field1': i, 'key':key }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (response.status, response.reason)
        conn.close()
    except:
        print("error at posting command")
