import json,httplib
import time
import os, sys
wo = open("parsy", "r")
with wo as me:
  for line in me:
    string = wo.readline()
    parsing = string.split(" ")
    c = [float(e) for e in parsing]
    coll_lat, coll_long, coll_dBm = c
    print str(coll_dBm)
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/Stren_Loc', json.dumps({
           "latitude": float(coll_lat),
           "longitude": float(coll_long),
           "strength": float("-"+str(coll_dBm)),
         }), {
           "X-Parse-Application-Id": "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM",
           "X-Parse-REST-API-Key": "4WhVWtKsId73kCjKAdwdN9ORKcJbR2fsU4PToOVw",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
wo.close()
print "bye"
