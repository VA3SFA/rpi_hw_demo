import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


ledpin = 18
freq = 50
GPIO.setup(ledpin, GPIO.OUT)
pwm = GPIO.PWM(ledpin, freq)
pwm.start(100)
time.sleep(1)

try:
    while True:
	for brightness in range(100):
            pwm.ChangeDutyCycle(brightness)
            time.sleep(0.15)
	for brightness in range(100):
            pwm.ChangeDutyCycle(brightness)
            time.sleep(0.15)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()        
