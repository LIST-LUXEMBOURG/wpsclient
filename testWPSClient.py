'''
Created on Aug 29, 2012

@author: desousa
'''

import WPSClient

cli = WPSClient.WPSClient(
    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
    "ogrbuffer", 
    ("size", "data"), 
    ("1", "http%3A%2F%2Fservices.iguess.tudor.lu%2Fpywps%2FsampleData%2FsampleLineRotterdam.xml"))

# Needed because PyWPS deletes CRS information from the outputs
cli.epsg = "28992"

cli.sendRequest()

print "Results of sendRequest():"
print cli.UUID
print cli.request

cli.generateMapFile()

print "Generated the map file."