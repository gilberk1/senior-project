import json,httplib
import time
import os, sys

with open("parsy", "r") as f:
  for line in f:
    string = wo.readline()
    parsing = string.split(" ")
    c = [float(e) for e in parsing]
    coll_lat, coll_long, coll_dBm = c

    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/Stren_Loc', json.dumps({
           "latitude": coll_lat,
           "longitude": coll_long,
           "strength": coll_dBm ,
         }), {
           "X-Parse-Application-Id": "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM",
           "X-Parse-REST-API-Key": "4WhVWtKsId73kCjKAdwdN9ORKcJbR2fsU4PToOVw",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())
