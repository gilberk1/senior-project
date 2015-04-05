import os, sys
import subprocess
from gps import *
from time import *
import time
import threading

gpsd = None 
os.system('clear')
fo = open("filin2", "w")
 
gpsd = None #seting the global variable
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      
i = 1

if __name__ == '__main__':
  gpsp = GpsPoller() 
  try:
    gpsp.start()
    while True:
 
        os.system('clear')
 
        print 'latitude    ' , gpsd.fix.latitude
        print 'longitude   ' , gpsd.fix.longitude
        print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        print 'altitude (m)' , gpsd.fix.altitude
        fo.write("GPS reading\n")
        fo.write("----------------------------------------\n")
        fo.write("latitude\n")
        fo.write('%d' % gpsd.fix.latitude)
        fo.write("\n")
        fo.write("longitude\n")
        fo.write('%d' % gpsd.fix.longitude)
        fo.write("\n")
        fo.write("time utc\n")
        fo.write('%d' % gpsd.utc,' + ', gpsd.fix.time)
        fo.write("\n")
        fo.write("altitude (m) \n")
        fo.write('%d' % gpsd.fix.altitude)
        fo.write("\n")       
    
        # Wifi Stuff Here
        #     
        #     
        # 

        print i
        fo.write('%d' % i)
        fo.write("\n")
        i = i + 1
        # print result
        time.sleep(2)

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    print "hi"
  print "Done.\nExiting."
