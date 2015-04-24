import json,httplib
import time
import os, sys

wo = open("parsy", "r")



connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/classes/Stren_Loc', json.dumps({
       "latitude": gpsd.fix.latitude,
       "longitude": gpsd.fix.longitude,
       "strength": coll_dBm ,
     }), {
       "X-Parse-Application-Id": "W0daAi5gvdhSxp5DDXhILsSyrfhzAaE3nhyePONM",
       "X-Parse-REST-API-Key": "4WhVWtKsId73kCjKAdwdN9ORKcJbR2fsU4PToOVw",
       "Content-Type": "application/json"
     })
result = json.loads(connection.getresponse().read())
