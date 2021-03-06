# encoding=utf8
import os, sys
import subprocess
from time import *
import time
import threading
import json,httplib
import serial
from gps import *
import RPi.GPIO as GPIO
import commands

# Surveying program script
# https://www.raspberrypi.org/forums/
# script initializes gps, wi-fi module for use
# script collects specific information from gps and wi-fi module
# script writes information to parsy file for future upload to Parse

# Setting pins for use
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Instantiate variables for button and counter
button_previous = 1
button_current = 1
brojac = 0
flag_pressed = 0
i = 1

gpsd = None #seting the global variable
port = serial.Serial("/dev/ttyAMA0", baudrate=19200) # Opening the serial port
start = ";"
stop = "#"

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

#While loop that collects data and writes and reads to/from a file
#Also includes shutdown button for exit
while True:
        os.system('rm -r /home/pi/Ras/collected')
        os.system('rm -r /home/pi/Ras/pearly')
        os.system('touch /home/pi/Ras/collected')
        os.system('touch /home/pi/Ras/pearly')
 
        gpsp = GpsPoller()
        gpsp.start()
        #Collect data from GPS
        lat = str(gpsd.fix.latitude)
        lon = str(gpsd.fix.longitude)       
        fo = open("/home/pi/Ras/viewlog", "a+")
        fo.write("GPS reading\n")
        fo.write("----------------------------------------\n")
        fo.write("latitude\n")
        fo.write(lat)
        fo.write("\n")
        fo.write("longitude\n")
        fo.write(lon)
        fo.write("\n")
        fo.write("time utc\n")
        fo.write(str(time))
        fo.write("\n")               
    
        interface = "wlan0"

        def get_name(cell):
            return matching_line(cell,"ESSID:")[1:-1]     

        #After grabbing quality cell, takes the value and converts it to dBm
        def get_dBm(cell):
            the_line = matching_line(cell,"Quality=")
            if the_line is not None:
                quality = the_line.split()[0].split('/')
                qual = int(round(float(quality[0]) / float(quality[1]) * 100))
                if qual <= 0:
                    return str(-100).rjust(3)
                elif qual >= 100:
                    return str(-50).rjust(3)
                else:
                    return str((qual/2)-100).rjust(3)

        def get_encryption(cell):
            enc=""
            if matching_line(cell,"Encryption key:") == "off":
                enc="Open"
            else:
                for line in cell:
                    matching = match(line,"IE:")
                    if matching!=None:
                        wpa2=match(matching,"IEEE 802.11i/WPA2 Version ")
                        if wpa2!=None:
                            #enc="WPA2 v."+wpa2
                            enc="WPA2"
                        wpa=match(matching,"WPA Version ")
                        if wpa!=None:
                            enc="WPA v."+wpa
                if enc=="":
                    enc="WEP"
            return enc

        def get_address(cell):
             return matching_line(cell,"Address: ")

        # Dictionary
        rules={"Name":get_name,
               "dBm":get_dBm,
               "Encryption":get_encryption,
               "Address":get_address,
               }

        def sort_cells(cells):
            sortby = "dBm"
            reverse = True
            cells.sort(None, lambda el:el[sortby], reverse)

        columns=["Name","Address","dBm","Encryption"]

        def matching_line(lines, keyword):
            """Returns the first matching line in a list of lines. See match()"""
            for line in lines:
                matching=match(line,keyword)
                if matching!=None:
                    return matching
            return None

        def match(line,keyword):
            """If the first part of line (modulo blanks) matches keyword,
            returns the end of that line. Otherwise returns None"""
            line=line.lstrip()
            length=len(keyword)
            if line[:length] == keyword:
                return line[length:]
            else:
                return None

        def parse_cell(cell):
            """Applies the rules to the bunch of text describing a cell and returns the
            corresponding dictionary"""
            parsed_cell={}
            for key in rules:
                rule=rules[key]
                parsed_cell.update({key:rule(cell)})
            return parsed_cell

        def mtar():
            
            cells=[[]]
            parsed_cells=[]

            proc = subprocess.Popen(["iwlist", "wlan0", "scan"],stdout=subprocess.PIPE, universal_newlines=True) #Using iwlist scanning command
            out, err = proc.communicate()

            for line in out.split("\n"):
                cell_line = match(line,"Cell ")
                if cell_line != None:
                    cells.append([])
                    line = cell_line[-27:]
                cells[-1].append(line.rstrip())

            cells=cells[1:]

            for cell in cells:
                parsed_cells.append(parse_cell(cell))

            sort_cells(parsed_cells)

            #Writing collected data to file
            so = open("/home/pi/Ras/collected", "w")
            for cell in cells:
                # name cell
                sa = str(get_name(cell))
                da = str(get_dBm(cell))
                ga = str(get_address(cell))
                so.write(sa)
                so.write(" ")
                so.write(da)
                so.write(" ")
                so.write(ga)
                so.write("\n")
            so.close()

            #grep through collected data, "TCNJ-DOT1X" with the lowest dBm value
            grep_com = commands.getoutput('grep -i TCNJ-DOT1X /home/pi/Ras/collected | grep -v None | sort -n -r -k 2 > /home/pi/Ras/pearly')
            #Read the first line in the file and grab the dBm and address value from it
            yo = open("/home/pi/Ras/pearly", "r")
            string = yo.readline()
            coll_dBm = string[12:14]
            print coll_dBm
            coll_address = string[15:]
            print coll_address
            yo.close()
            if coll_dBm == "  ":
               coll_dBm = NAN
            fo.write("Wifi reading\n")
            fo.write("----------------------------------------\n")
            fo.write("dBm\n")
            fo.write(coll_dBm)
            fo.write("\n")
            fo.write("Address\n")
            fo.write(coll_address)
            fo.write("\n")
            
            #Append the lat, long, and dBm values on a file that will be later read and then uploaded to parse
            wo = open("/home/pi/Ras/parsy", "a")
            wo.write(str(gpsd.fix.latitude))
            wo.write(" ")
            wo.write(str(gpsd.fix.longitude))
            wo.write(" ")
            wo.write(coll_dBm)
            wo.write("\n")
            wo.close()

            #Write the collected values to the GPIO pins of the raspberry pi
            port.write(start+str(coll_dBm)+":"+str(gpsd.fix.latitude)+"!"+str(gpsd.fix.longitude)+stop)

        mtar()   
        fo.write("end entry\n")
        print "end entry\n"
        fo.close()

        #Flash LED
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.5)    
        GPIO.output(18, GPIO.LOW)
        
        #Shutdown Button
        button_current = GPIO.input(25);
        flag_pressed = button_previous + button_current

        if (not(flag_pressed)):
           brojac += 1
        else:
           brojac = 0

        if ((not flag_pressed) and  brojac >= 3):
           wo = open("/home/pi/Ras/parsy", "a")
           wo.write("ended collect\n")
           wo.close()
           open('/home/pi/Ras/pearly', 'w').close()
           open('/home/pi/Ras/collected', 'w').close()
           os.system("sudo shutdown -h now")
           break

        button_previous = button_current
        time.sleep(0.3)
