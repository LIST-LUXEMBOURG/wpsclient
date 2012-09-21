'''
Created on Sep 20, 2012

@author: desousa
'''

import WPSClient
import time

cli = WPSClient.WPSClient(
    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
    "test_rand_map", 
    ["delay"], 
    ["1"])

cli.sendRequest()

while not cli.checkStatus():
    print "Waiting..."
    time.sleep(10)
    
print "Results of sendRequest():"
print cli.UUID
print cli.request

# Needed because PyWPS deletes CRS information from the outputs
# Maybe it should be a parameter to the constructor?
cli.epsg = "28992"

cli.generateMapFile()

print "Successfully generated the map file:"
print cli.getMapFilePath()