import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


ledpin = 18
GPIO.setup(ledpin, GPIO.OUT)

try:
    while True:
        GPIO.output(ledpin, 1)
        time.sleep(0.5)
        GPIO.output(ledpin, 0)
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()        
