'''
Created on Aug 29, 2012

@author: desousa
'''

import WPSClient

cli = WPSClient.WPSClient("http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", \
                "ogrbuffer", \
                ("size", "data"), \
                ("1", "http%3A%2F%2Fservices.iguess.tudor.lu%2Fpywps%2FsampleData%2FsampleLineRotterdam.xml"))

print "\n\n The constructor reached the end"
print cli.UUID
print cli.request

cli.generateMapFile()

print "Generated the Map file."