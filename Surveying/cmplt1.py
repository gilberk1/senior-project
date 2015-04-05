import os, sys
import subprocess
from gps import *
from time import *
import time
import threading
import json,httplib
import serial

#pointing to the gps module
sudo killall gpsd
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

fo = open("mainfile", "w+")
do = open("log", "r")

gpsd = None 
os.system('clear')
