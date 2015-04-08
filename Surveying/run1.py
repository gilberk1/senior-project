import os, sys
import subprocess
from time import *
import time
import threading
import json,httplib


fo = open("filin1", "rw+")

lat = 32.93
lon = 40.93
stren = -60
i = 1

if __name__ == '__main__':
  try:
    gpsp.start()
  except Exception, r:
    print "no GPS found continuing with procedure"
    print r
    while True:
 
        os.system('clear')
    
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

        # Try to upload to Parse
        try:
            connection = httplib.HTTPSConnection('api.parse.com', 443)
            connection.connect()
            connection.request('POST', '/1/classes/Stren_Loc', json.dumps({
                   "latitude": lat,
                   "longitude": lon,
                   "strength": stren,
                 }), {
                   "X-Parse-Application-Id": "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM",
                   "X-Parse-REST-API-Key": "4WhVWtKsId73kCjKAdwdN9ORKcJbR2fsU4PToOVw",
                   "Content-Type": "application/json"
                 })
            result = json.loads(connection.getresponse().read())
        except Exception, e:
            print "there was an error connecting to parse"
            print e

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

            so = open("namefil", "r+")
            for cell in cells:
                # name cell
                sa = str(get_name(cell))
                so.write(sa)
                so.write("\n")
            so.close()
            do = open("dBmfil", "r+")
            for cell in cells:
                # dBm cell
                da = str(get_dBm(cell))
                do.write(da)
                do.write("\n")
            do.close()
            go = open("addressfil", "r+")
            for cell in cells:
                # address cell
                ga = str(get_address(cell))
                go.write(fa)
                go.write("\n")
            go.close()

        mtar()
        i = i + 1
        print i
        fo.write('%d' % i)
        fo.write("\n")
        fo.write("end entry\n")
        print "end entry\n"

        so.seek(0,0)
        li = so.readline(19)
        so.next()
        fi = so.readline(19)
        so.next()
        gi = so.readline(19)
        #so.next()
        if li == "IsthistheKrustyKrab":
            first_dBm = do.readline(4)
            first_address = go.readline(34)
        	pass
        if fi == "IsthistheKrustyKrab":        	
        	point = do.next()
        	point = go.next()
        	second_dBm = do.readline(4)
            second_address = go.readline(34)
        	pass
        if gi == "IsthistheKrustyKrab":       	
        	point = do.next()
        	point = do.next()
        	point = go.next()
        	point = go.next()
            third_dBm = do.readline(4)
            third_address = go.readline(34) 
        	pass

        # #Sifting through Output textfile to find TCNJ-DOT1X data
        # if line1 == "TCNJ-DOT1X" || line2 == "TCNJ-DOT1X" || line3 == "TCNJ-DOT1X" :
        #     pointer = int(fo.tell())
        #     fo.seek(4+pointer,0)
        #     dbm_val = fo.readline()
        #     fo.write(dbm_val)
        #     fo.write("\n")
        #     pointer = int(fo.tell())
        #     fo.seek(4+pointer,0)
        #     address_val = fo.readline()
        #     fo.write(address_val)
        #     fo.write("\n")
        #     fo.write("complete\n")
            
        # 	pass
        time.sleep(2)

  except (KeyboardInterrupt, SystemExit): 
    print "\nKilling Thread..."
    fo.close()
  print "Done.\nExiting."
