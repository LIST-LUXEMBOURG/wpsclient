'''
Created on Aug 28, 2012

@author: Luis de Sousa [luis.desousa@tudor.lu]
'''

__all__ = ["Tags","Output","DataSet","MapServerText"]

import os
import urllib2
import httplib
from ConfigParser import SafeConfigParser
from Tags import Tags
from Output import ComplexOutput
from Output import LiteralOutput
from XMLPost import XMLPost
import MapServerText as UMN
import DataSet as GDAL

DEBUG = True

##########################################################

class WPSClient:
    """ """
    
    map  = None
    epsg = None
    serverAddress = None
    processName = None
    inputNames = None
    inputValues = None
    outputNames = None
    xmlPost = None
    request = None
    statusURL = None
    processId = None
    percentCompleted = 0
    resultsComplex = []
    resultsLiteral = []
    
    #Configs
    pathFilesGML = ""
    mapServerURL = ""
    mapFilesPath = ""
    mapTemplate  = ""
    imagePath    = ""
    imageURL     = ""
    otherProjs   = ""
    
    def __init__(self):
         
        self.loadConfigs()
        
    def init(self, serverAddress, processName, inputNames, inputValues, outputNames):
        
        self.serverAddress = serverAddress
        self.processName = processName
        self.inputNames = inputNames
        self.inputValues = inputValues
        self.outputNames = outputNames
        
    def initFromURL(self, url):
        
        self.statusURL = url
        self.processId = self.decodeId(url)
        
    def loadConfigs(self):
        """ Loads default values from the configuration file. """
        
        parser = SafeConfigParser()
        parser.read('WPSClient.cfg')
    
        self.pathFilesGML = parser.get('Data',      'GMLfilesPath')
        self.mapServerURL = parser.get('MapServer', 'MapServerURL')
        self.mapFilesPath = parser.get('MapServer', 'mapFilesPath')
        self.mapTemplate  = parser.get('MapServer', 'mapTemplate')
        self.imagePath    = parser.get('MapServer', 'imagePath')
        self.imageURL     = parser.get('MapServer', 'imgeURL')
        self.otherProjs   = parser.get('MapServer', 'otherProjs')
        
    def decodeId(self, url):
        
        s = url.split("/")
        return s[len(s) - 1].split(".")[0] 
        
    def buildRequest(self):
        
        if len(self.inputNames) <> len(self.inputValues):
            print "Different number of input names and values."
            return
        
        self.xmlPost = XMLPost(self.processName)
        
        for i in range(0, len(self.inputNames)):
            if ("http://" in self.inputValues[i]): 
                self.xmlPost.addRefInput(self.inputNames[i], self.inputValues[i])
            else:
                self.xmlPost.addLiteralInput(self.inputNames[i], self.inputValues[i])
        
        for o in self.outputNames:
            self.xmlPost.addOutput(o)
            
    def sendRequest(self):
        
        self.buildRequest()
        
        if(self.xmlPost == None):
            print "It wasn't possible to build a request with the given arguments"
            return None
        
        request = self.xmlPost.getString()
        if(request == None):
            print "It wasn't possible to build a request with the given arguments"
            return None
        
        rest = self.serverAddress.replace("http://", "")     
        split = rest.split("/")
        
        if(len(split) < 2):
            print "It wasn't possible to process the server address"
            return None
        
        host = split[0]
        
        api_url = rest.replace(host, "", 1)        
        api_url = api_url.replace("?", "")
        
        if DEBUG:
            print "API: " + api_url
            print "HOST: " + host
            print "Sending the request:\n"
            print request + "\n"
        
        webservice = httplib.HTTP(host)
        webservice.putrequest("POST", api_url)
        webservice.putheader("Host", host)
        webservice.putheader("User-Agent","Python post")
        webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % len(request))
        webservice.endheaders()
        webservice.send(request)
        statuscode, statusmessage, header = webservice.getreply()
        self.xmlResponse = webservice.getfile().read()
        
        if DEBUG:
            print "Request results:"
            print statuscode, statusmessage, header
            print self.xmlResponse
        
        self.statusURL = self.xmlResponse.split("statusLocation=\"")[1].split("\"")[0]
        self.processId = self.decodeId(self.statusURL)
        
        return self.statusURL  

    def checkStatus(self):
        
        if (self.statusURL == None):
            print "To soon to ask for status"
            return False
        
        r = urllib2.urlopen(urllib2.Request(self.statusURL))
        self.xmlResponse = r.read()
        r.close()
        
        #Check if the process failed
        if (Tags.preFail in self.xmlResponse):
            print "The process failed with the following message:"
            print self.xmlResponse.split(Tags.preFail)[1].split(Tags.sufFail)[0]
            return True
           
        #Check if the process has finished
        if not (Tags.preSucc in self.xmlResponse):
            print "The process hasn't finished yet."
            if ("percentCompleted" in self.xmlResponse):
                self.percentCompleted = self.xmlResponse.split("percentCompleted=\"")[1].split("\"")[0]
                print str(self.percentCompleted) + " % of the execution complete."
            return False
        
        if DEBUG:
            print "The process has finished successfully."
            print "Processing the results..."
        
        #Process the results
        outVector = self.xmlResponse.split(Tags.preOut)
        for o in outVector:
            if o.count(Tags.preLit) > 0:
                self.resultsLiteral.append(LiteralOutput(o))
            elif o.count(Tags.preCplx) > 0:
                self.resultsComplex.append(ComplexOutput(o, self.processId))
            # Reference outputs
            elif o.count(Tags.preRef) > 0:
                # Assumes that Complex outputs have a mimeType
                if o.count("mimeType") > 0:
                    self.resultsComplex.append(ComplexOutput(o, self.processId))
                else:
                    self.resultsLiteral.append(LiteralOutput(o))
                    
        # Save complex outputs to disk
        for c in self.resultsComplex:
            c.saveToDisk(self.pathFilesGML)
                    
        return True           
            
        
    def generateMapFile(self):
        """
        :returns: The path to the map file generated.
        """
        
        self.map = UMN.MapFile(self.processId)
        
        self.map.shapePath    = self.pathFilesGML
        self.map.epsgCode     = self.epsg
        self.map.mapTemplate  = self.mapTemplate
        self.map.imagePath    = self.imagePath
        self.map.imageURL     = self.imageURL
        self.map.mapServerURL = self.mapServerURL
        self.map.mapFilesPath = self.mapFilesPath
        self.map.otherProjs   = self.otherProjs
        
        for c in self.resultsComplex:
            
            ds = GDAL.DataSet(c.path)
            
            if ds.dataType == "vector":
                style = UMN.MapStyle()
                layer = UMN.VectorLayer(c.path, ds.getBBox(), ds.getEPSG(), c.name)
                type = str(ds.getGeometryType())
                if type <> None:
                    layer.layerType = type
                else:
                    layer.layerType = "Polygon"
                print "The layer type: " + str(ds.getGeometryType())
                layer.addStyle(style)
                self.map.addLayer(layer)
              
            elif ds.dataType == "raster":
                layer = UMN.RasterLayer(c.path, ds.getBBox(), ds.getEPSG(), c.name)
                self.map.addLayer(layer)
                
            else:
                print "Warning: couldn't determine the type of Complex output " + c.name
                  
        
        self.map.writeToDisk()
        
        if DEBUG:
            print "Wrote map file to disk:\n" + self.map.filePath()
            
        return self.map.filePath()
        
    def getMapFilePath(self):
       
        if self.map <> None:
            return self.map.filePath()
        else:
            return None     
    
    