import os, sys
import subprocess
from gps import *
from time import *
import time
import threading

gpsd = None 
os.system('clear')
 
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
    while True:
 
        os.system('clear')
 
        print
        print ' GPS reading'
        print '----------------------------------------'
        print 'latitude    ' , gpsd.fix.latitude
        print 'longitude   ' , gpsd.fix.longitude
        print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        print 'altitude (m)' , gpsd.fix.altitude
 
        
        interface = "wlan0"

        def get_name(cell):
            return matching_line(cell,"ESSID:")[1:-1]

        #need to convert quality to dBm
        def get_dBm(cell):
            quality = matching_line(cell,"Quality=").split()[0].split('/')
            qual = int(round(float(quality[0]) / float(quality[1]) * 100))
            if: qual <= 0
                return str(-100).rjust(3)
            else if: qual >= 100
                return str(-50).rjust(3)
            else:
                return str((qual/2)-100).rjust(3)

        def get_channel(cell):
            frequency = matching_line(cell,"Frequency:")
            channel = frequency[frequency.index("(")+9:frequency.index(")")]
            return channel

        def get_signal_level(cell):
            level = matching_line(cell,"Quality=").split("Signal level=")[1]
            level = level.split()[0].split('/')
            return str(int(round(float(level[0]) / float(level[1]) * 100))).rjust(3) + " %"

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
               "Channel":get_channel,
               "Encryption":get_encryption,
               "Address":get_address,
               "Signal":get_signal_level
               }

        def sort_cells(cells):
            sortby = "dBm"
            reverse = True
            cells.sort(None, lambda el:el[sortby], reverse)

        columns=["Name","Address","dBm","Signal", "Channel","Encryption"]

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

            print_cells(parsed_cells)

        print
        print ' Wifi reading'
        print '----------------------------------------'
        mtar()

        time.sleep(4) 
         
  except (KeyboardInterrupt, SystemExit): 
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join()
  print "Done.\nExiting."