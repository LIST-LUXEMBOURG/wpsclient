'''
Created on Sep 26, 2012

@author: desousa
'''

import WPSClient
import time

iniCli = WPSClient.WPSClient()

# Basic test with literal inputs
#iniCli.init(
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    "test_rand_map", 
#    ["delay"], 
#    ["1"],
#    ["rand", "region", "num"],
#    ["rand", "region", "num"])

# Test with a remote GML resource
#iniCli.init(
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    "buffer", 
#    ["size","data"], 
#    ["5","http://services.iguess.tudor.lu/pywps/sampleData/testLines4326.gml"],
#    ["buffer"])

# Test with a WFS resource
#iniCli.init(
#    # Process Server address
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    # Process name
#    "buffer", 
#    # Input names
#    ["size","data"], 
#    # Input values - '&' character must be passed as '&amp;'
#    ["5","http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/Europe4326.map&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=getfeature&amp;TYPENAME=testLines4326&amp;srsName=EPSG:900913&amp;MAXFEATURES=10"],
#    # Output names
#    ["buffer"])

# Test with ultimate question
#iniCli.init(
#    # Process Server address
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    # Process name
#    "ultimatequestionprocess", 
#    # Input names
#    [], 
#    # Input values - '&' character must be passed as '&amp;'
#    [],
#    # Output names
#    ["answer"])

# Test with solar cadastre segmentation
#iniCli.init(
#    # Process Server address
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    # Process name
#    "solar_cadastre_segment", 
#    # Input names
#    ["dsm","roof_training_area","building_footprints","roof_training_area_col"], 
#    # Input values - '&' character must be passed as '&amp;'
#    ["http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/RO_localOWS_test.map&amp;SERVICE=WCS&amp;VERSION=1.0.0&amp;REQUEST=GetCoverage&amp;IDENTIFIER=ro_dsm_mini&amp;FORMAT=image/tiff&amp;BBOX=92217,436688,92313,436772&amp;CRS=EPSG:28992&amp;RESX=1&amp;RESY=1",
#     "http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/RO_localOWS_test.map&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=getfeature&amp;TYPENAME=RO_training_areas_mini&amp;srsName=EPSG:28992",
#     "http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/RO_localOWS_test.map&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=getfeature&amp;TYPENAME=RO_building_footprints_mini&amp;srsName=EPSG:28992",
#     "type"],
#    # Output names
#    ["optimum_aspect", "optimum_slope", "ro_roof_useful_intsect_gml"],
#    ["aspectMap","slopeMap","usefulRoofAreas"])

## Test with solar cadastre single process
#iniCli.init(
#    # Process Server address
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    # Process name
#    "solar_cadastre", 
#    # Input names
#    ["dsm", "roof_training_area", "roof_training_area_col", "building_footprints", "month"], 
#    # Input values - '&' character must be passed as '&amp;'
#    ["http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/RO_localOWS_test.map&amp;SERVICE=WCS&amp;VERSION=1.0.0&amp;REQUEST=GetCoverage&amp;IDENTIFIER=ro_dsm_mini&amp;FORMAT=image/tiff&amp;BBOX=92217,436688,92313,436772&amp;CRS=EPSG:28992&amp;RESX=1&amp;RESY=1",
#     "http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/RO_localOWS_test.map&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=getfeature&amp;TYPENAME=RO_training_areas_mini&amp;srsName=EPSG:28992",
#     "type",
#     "http://services.iguess.tudor.lu/cgi-bin/mapserv?map=/var/www/MapFiles/RO_localOWS_test.map&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=getfeature&amp;TYPENAME=RO_building_footprints_mini&amp;srsName=EPSG:28992",
#     "7"
#     ],
#    # Output names
#    ["solar_irradiation"],
#    #Output titles
#    ["MySolarIrradiationMap"])

# Test with noise process
#iniCli.init(
#    # Process Server address
#    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
#    # Process name
#    "noise", 
#    # Input names
#    ["input"], 
#    # Input values - '&' character must be passed as '&amp;'
#    ["http://services.iguess.tudor.lu/pywps/sampleData/lb_dem_10m_small.tiff"],
#    # Output names
#    ["noise"],
#    #Output titles
#    ["NoisyMap"])

# Test asynchronous processing
iniCli.init(
    "http://services.iguess.tudor.lu/cgi-bin/pywps.cgi?", 
    "test_status", 
    ["delay"], 
    ["500"],
    ["num"],
    ["num"])

url = ""
url = iniCli.sendRequest()

iniCli = None

if(url == None):
    print "Sorry something went wrong with the request."

else:
    
    statCli = WPSClient.WPSClient()
    
    statCli.initFromURL(url,["solar_irradiation"],["MySolarIrradiationMap"])
#    statCli.initFromURL('http://services.iguess.tudor.lu/wpsoutputs/pywps-7f8394a2-2ff3-11e2-8730-005056a512c1.xml',
#                        ["solar_irradiation"],
#                        ["MySolarIrradiationMap"])

    while not statCli.checkStatus():
        print "Process still running"
        print str(statCli.percentCompleted) + "% completed"
        print "Status message: " + str(statCli.statusMessage)
        time.sleep(10)
        
    if(statCli.status == statCli.ERROR):
        print "There was an error. No mapfile was generated."
    
    else:
        # Needed because PyWPS deletes CRS information from the outputs
        # Maybe it should be a parameter to the constructor?
        statCli.epsg = "28992"
        
        path = statCli.generateMapFile()
        print "Wrote map file to disk:\n" + path
    
    
    
    
    
    
    