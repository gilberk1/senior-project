import os, sys
import subprocess
from gps import *
from time import *
import time
import threading
import json,httplib
import serial

gpsd = None 
os.system('clear')
fo = open("filin1", "w")
po = open("wptr", "w")

port = serial.Serial("/dev/ttyAMA0", baudrate=19200)
start = ";"
stop = "#"
interface = "wlan0"
 
class GpsPoller(threading.Thread):
 def __init__(self):
   threading.Thread.__init__(self)
   global gpsd #bring it in scope
   gpsd = gps(mode=WATCH_ENABLE)
   self.current_value = None
   self.running = True

 def run(self):
   global gpsd
   while gpsp.running:
     gpsd.next() 

if __name__ == '__main__':
  gpsp = GpsPoller() 
  try:
    gpsp.start()
  except Exception, r:
    print "no GPS found continuing with procedure"
    print r
    while True:
 
        os.system('clear')
