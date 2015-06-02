# Python script that takes the parsy script from surv_script.py and uploads its contents to parse

from __future__ import division
import json,httplib
import time
import os, sys
wo = open("parsy", "r")
with open("parsy","r") as f:
  	for line in f:
    		string = wo.readline()
    		parsing = string.split(" ")
    		c = [float(e) for e in parsing]
    	  coll_lat, coll_long, coll_dBm = c
    	  # applying calibration
    		a = coll_dBm/10
    		base = 5
    		exp = a - base
    		calc = 5*pow(2,exp)
    		bench = coll_dBm + calc
    		bench_dBm = round(bench)
    		print bench_dBm
    		connection = httplib.HTTPSConnection('api.parse.com', 443)
    		connection.connect()
    		connection.request('POST', '/1/classes/Location', json.dumps(
{
           		"latitude": float(coll_lat),
           		"longitude": float(coll_long),
           		"strength": float("-"+str(bench_dBm)),
         	}),
{
           		"X-Parse-Application-Id": "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM",
           		"X-Parse-REST-API-Key": "4WhVWtKsId73kCjKAdwdN9ORKcJbR2fsU4PToOVw",
           		"Content-Type": "application/json"
         	})
    	result = json.loads(connection.getresponse().read())
wo.close()
print "bye"
