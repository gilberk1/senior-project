import serial
import time

port = serial.Serial("/dev/ttyAMA0", baudrate=115200)
start = ";"
stop = "#"

while True:
    port.write(start+"dBm"+":"+"lat"+"!"+"long"+stop)
    time.sleep(2)
    port.write(start+"dBm"+":"+"lat"+"!"+"long"+stop)
    time.sleep(2)
