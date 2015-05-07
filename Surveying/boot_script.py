import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)

button_previous = 1
button_current = 1
brojac = 0
flag_pressed = 0
i = 1

while i < 25:

    GPIO.output(18, GPIO.HIGH)
    time.sleep(2)    
    GPIO.output(18, GPIO.LOW)
    time.sleep(2)
    i = i +1
    button_current = GPIO.input(25);
    flag_pressed = button_previous + button_current
    if (not(flag_pressed)):
      brojac += 1
    else:
      brojac = 0

    if ((not flag_pressed) and  brojac >= 4):
      #print("Shutdown")
      os.system("sudo shutdown -h now")
      break

    button_previous = button_current   
GPIO.cleanup()