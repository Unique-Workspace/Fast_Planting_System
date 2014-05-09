import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

RGB_R = GPIO.PWM(15, 50)  # channel=15 frequency=50Hz
RGB_G = GPIO.PWM(16, 50)  # channel=16 frequency=50Hz
RGB_B = GPIO.PWM(18, 50)  # channel=18 frequency=50Hz
RGB_R.start(0)
RGB_G.start(0)
RGB_B.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            RGB_R.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_R.ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 101, 5):
            RGB_G.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_G.ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 101, 5):
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 101, 5):
            RGB_R.ChangeDutyCycle(dc)
            RGB_G.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_R.ChangeDutyCycle(dc)
            RGB_G.ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 101, 5):
            RGB_R.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_R.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 101, 5):
            RGB_G.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_G.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)

        for dc in range(0, 101, 5):
            RGB_R.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            RGB_R.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            RGB_B.ChangeDutyCycle(dc)
            time.sleep(0.1)

except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()