'''
Created on Sep 26, 2012

@author: desousa
'''

import WPSClient
import time

iniCli = WPSClient.WPSClient()

print iniCli.decodeId("http://services.iguess.tudor.lu/wpsoutputs/pywps-a3eddbc8-031a-11e2-a36a-005056a512c1.xml")

# Basic test with literal inputs
#iniCli.init(
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    "test_rand_map", 
#    ["delay"], 
#    ["1"],
#    ["rand", "region", "num"])

# Test with a remote GML resource
#iniCli.init(
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    "buffer", 
#    ["size","data"], 
#    ["5","http://services.iguess.tudor.lu/pywps/sampleData/testLines4326.gml"],
#    ["buffer"])

# Test with a WFS resource
iniCli.init(
    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
    "buffer", 
    ["size","data"], 
    ["5","http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/Europe4326.map&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=getfeature&amp;TYPENAME=testLines4326&amp;srsName=EPSG:900913&amp;MAXFEATURES=10"],
    ["buffer"])

url = iniCli.sendRequest()

iniCli = None

if(url == None):
    print "Sorry something went wrong."

else:
    
    statCli = WPSClient.WPSClient()
    
    statCli.initFromURL(url)

    while not statCli.checkStatus():
        print "Waiting..."
        time.sleep(10)
    
    # Needed because PyWPS deletes CRS information from the outputs
    # Maybe it should be a parameter to the constructor?
    statCli.epsg = "28992"
    
    statCli.generateMapFile()
    
    print "Successfully generated the map file:"
    print statCli.getMapFilePath()