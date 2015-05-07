import os, sys
import subprocess
# from gps import *
from time import *
import time
import threading
# import serial


# gpsd = None 
os.system('clear')
# fo = open("filin2", "rw+")
#do = open("filee", "rw+")
 
# gpsd = None #seting the global variable
os.system('clear') #clear the terminal (optional)

# port = serial.Serial("/dev/ttyAMA0", baudrate=19200)
# start = ";"
# stop = "#"
 
# class GpsPoller(threading.Thread):
#   def __init__(self):
#     threading.Thread.__init__(self)
#     global gpsd #bring it in scope
#     gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
#     self.current_value = None
#     self.running = True #setting the thread running to true
 
#   def run(self):
#     global gpsd
#     while gpsp.running:
#       gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      
i = 1

if __name__ == '__main__':
  # gpsp = GpsPoller() 
  try:
    # gpsp.start()
    while True:
 
        # os.system('clear')
 
        # print 'latitude    ' , gpsd.fix.latitude
        # print 'longitude   ' , gpsd.fix.longitude
        # print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        # print 'altitude (m)' , gpsd.fix.altitude
        # fo.write("GPS reading\n")
        # fo.write("----------------------------------------\n")
        # fo.write("latitude\n")
        # fo.write('%d' % gpsd.fix.latitude)
        # fo.write("\n")
        # fo.write("longitude\n")
        # fo.write('%d' % gpsd.fix.longitude)
        # fo.write("\n")
        # fo.write("time utc\n")
        # fo.write('%d' % gpsd.utc,' + ', gpsd.fix.time)
        # fo.write("\n")
        # fo.write("altitude (m) \n")
        # fo.write('%d' % gpsd.fix.altitude)
        # fo.write("\n")       
    
        # Wifi Stuff Here
    
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

        def get_address(cell):
             return matching_line(cell,"Address: ")

        rules={"Name":get_name,
               "dBm":get_dBm,
               "Address":get_address,
               }

        def sort_cells(cells):
            sortby = "dBm"
            reverse = True
            cells.sort(None, lambda el:el[sortby], reverse)

        columns=["Name","Address","dBm"]

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

            cells=cells[1:4]

            for cell in cells:
                parsed_cells.append(parse_cell(cell))

            sort_cells(parsed_cells)
            # print_cells(parsed_cells)

            # for cell in cells:
            #     # name cell
            #     #print get_name(cell)
            #     # fo.write(str(get_name(cell)))
            #     #fo.write("\n")
            fo = open("filin2", "r+")
            for cell in cells:
                # dBm cell
                #print get_dBm(cell)
                vel = str(get_dBm(cell))
                fo.write(vel)
                fo.write("\n")
                # fo.write("\n")
                # value = str(get_dBm(cell))
                # fo.write(value)
                # fo.write("\n")
            fo.seek(0,0)
            li = fo.readline(3)
            
            print li
            fo.close()
            # for cell in cells:
            #     # address cell
            #     #print get_address(cell)
            #     # fo.write(str(get_address(cell)))
            #     #fo.write("\n")

        mtar()
        #li = do.readline()
        #port.write(start+val+":"+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude)+stop)


        # line1 = fo.readline()
        # fo.next()
        # line2 = fo.readline()
        # fo.next()
        # line3 = fo.readline()
        # #Sifting through Output textfile to find TCNJ-DOT1X data
        # if line1 == "IsthistheKrustyKrab" or line2 == "IsthistheKrustyKrab" or line3 == "IsthistheKrustyKrab" :
        #     pointer = int(fo.tell())
        #     fo.write("hi\n")
        #     print "hi"
        #     fo.seek(3+pointer,0)
        #     dbm_val = fo.readline()
        #     fo.write(dbm_val)
        #     fo.write("\n")
        #     pointer = int(fo.tell())
        #     fo.seek(3+pointer,0)
        #     address_val = fo.readline()
        #     fo.write(address_val)
        #     fo.write("\n")
        #     fo.write("complete\n")
        #     # port.write(start+str(dbm_val)+":"+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude)+stop)
            
        #     pass

        # Try to upload to Parse
        try:
            connection = httplib.HTTPSConnection('api.parse.com', 443)
            connection.connect()
            connection.request('POST', '/1/classes/Stren_Loc', json.dumps({
                   "latitude": str(gpsd.fix.latitude),
                   "longitude": str(gpsd.fix.longitude),
                   "strength": str(dbm_val),
                 }), {
                   "X-Parse-Application-Id": "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM",
                   "X-Parse-REST-API-Key": "4WhVWtKsId73kCjKAdwdN9ORKcJbR2fsU4PToOVw",
                   "Content-Type": "application/json"
                 })
            result = json.loads(connection.getresponse().read())
        except Exception, e:
            print "there was an error connecting to parse"
            print e

        print i
        #fo.write('%d' % i)
        #fo.write("\n")
        i = i + 1
        # print result
        time.sleep(2)

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    # gpsp.running = False
    # gpsp.join() # wait for the thread to finish what it's doing
    print "hi"
  print "Done.\nExiting."
