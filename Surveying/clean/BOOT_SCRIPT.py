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

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

button_previous = 1
button_current = 1
brojac = 0
flag_pressed = 0
i = 1

os.system('clear')

gpsd = None #seting the global variable
port = serial.Serial("/dev/ttyAMA0", baudrate=19200)
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

os.system('sudo killall gpsd')
os.system('sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock')

if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()
    while True:
        fo = open("/home/pi/Ras/viewlog", "a+")
        fo.write("GPS reading\n")
        fo.write("----------------------------------------\n")
        fo.write("latitude\n")
        fo.write(str(gpsd.fix.latitude))
        fo.write("\n")
        fo.write("longitude\n")
        fo.write(str(gpsd.fix.longitude))
        fo.write("\n")
        fo.write("time utc\n")
        fo.write("time")
        fo.write("\n")
        
    
        interface = "wlan0"

        def get_name(cell):
            return matching_line(cell,"ESSID:")[1:-1]     

        #Convert quality to dBm
        def get_dBm(cell):
            quality = matching_line(cell,"Quality=").split()[0].split('/')
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

        def print_table(table):
            widths=map(max,map(lambda l:map(len,l),zip(*table))) #functional magic

            justified_table = []
            for line in table:
                justified_line=[]
                for i,el in enumerate(line):
                    justified_line.append(el.ljust(widths[i]+2))
                justified_table.append(justified_line)
            
            for line in justified_table:
                for el in line:
                    print el,
                print

        def print_cells(cells):
            table=[columns]
            for cell in cells:
                cell_properties=[]
                for column in columns:
                    cell_properties.append(cell[column])
                table.append(cell_properties)
            print_table(table)

        def mtar():
            """Pretty prints the output of iwlist scan into a table"""
            
            cells=[[]]
            parsed_cells=[]

            proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
            out, err = proc.communicate()

            cells=cells[1:]

            for cell in cells:
                parsed_cells.append(parse_cell(cell))

            sort_cells(parsed_cells)

            so = open("/home/pi/Ras/collected_data", "r+")
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

            grep_com = commands.getoutput('grep -i TCNJ-DOT1X /home/pi/Ras/collected_data | sort –n -r -k 2 > /home/pi/Ras/tmp')
            yo = open("/home/pi/Ras/tmp", "r")
            string = yo.readline()
            coll_dBm = string[12:14]
            print coll_dBm
            coll_address = string[15:]
            print coll_address
            yo.close()
            fo.write("Wifi reading\n")
            fo.write("----------------------------------------\n")
            fo.write("dBm\n")
            fo.write(coll_dBm)
            fo.write("\n")
            fo.write("Address")
            fo.write(coll_address)
            fo.write("\n")
            
            wo = open("/home/pi/Ras/parsy", "a+")
            wo.write(gpsd.fix.latitude)
            wo.write(" ")
            wo.write(gpsd.fix.longitude)
            wo.write(" ")
            wo.write(coll_dBm)
            wo.write("\n")
            wo.close()

            port.write(start+str(coll_dBm)+":"+str(gpsd.fix.latitude)+"!"+str(gpsd.fix.longitude)+stop)

        mtar()   
        fo.write("end entry\n")
        print "end entry\n"
        fo.close()

        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.6)    
        GPIO.output(18, GPIO.LOW)
        button_current = GPIO.input(25);
        flag_pressed = button_previous + button_current

        if (not(flag_pressed)):
           brojac += 1
        else:
           brojac = 0

        if ((not flag_pressed) and  brojac >= 4):
           #print("Shutdown")
           GPIO.cleanup()
           open('/home/pi/Ras/tmp', 'w').close()
           open('/home/pi/Ras/collected_data', 'w').close()
           os.system("sudo shutdown -h now")
           break

        button_previous = button_current
        #print brojac        
        time.sleep(0.3)
