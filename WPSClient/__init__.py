'''
Created on Aug 28, 2012

@author: Luis de Sousa [luis.desousa@tudor.lu]
'''

__all__ = ["DataSet","MapServerText"]

from ConfigParser import SafeConfigParser
import urllib2
import uuid
import os
import MapServerText as UMN

###########################################################

class LiteralOutput:

    name = None
    value = None

    def __init__(self, rawString):

        self.name = rawString.split("<ows:Identifier>")[1].split("</ows:Identifier>")[0]
        self.value = rawString.split("<wps:LiteralData>")[1].split(">")[1].split("</wps:LiteralData>")[0].split("</wps:LiteralData")[0] 

###########################################################

class ComplexOutput:

    name = None
    value = None
    uniqueID = None
    path = None

    def __init__(self, rawString, unique):

        self.name = rawString.split("<ows:Identifier>")[1].split("</ows:Identifier>")[0]
        self.value = rawString.split("<wps:ComplexData>")[1].split("</wps:ComplexData>")[0]
        self.uniqueID = unique
        
        while self.value[0] <> "<":
            self.value = self.value[1:len(self.value)]

    def saveToDisk(self, dest):
        
        file = None
        self.path = os.path.join(dest, self.uniqueID + "_" + self.name + ".gml")
        
        try:
            file = open(self.path, 'w')
            file.write(self.value)
            print "Saved gml output file: %s\n" %self.path
        except Exception, err:
            print "Error saving %s:\n%s" %(self.path, err)
        finally:
            if file <> None:
                file.close()
                
        
        
##########################################################

class WPSClient:
    """ """
    
    UUID = None
    epsg = None
    request = None
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
    
    def __init__(self, serverAddress, processId, inputNames, inputValues):
        
        self.UUID = uuid.uuid1().__str__()
        
        self.loadConfigs()
        
    def loadConfigs(self):
        """ Loads default values from the configuration file. """
        
        parser = SafeConfigParser()
        parser.read('default.cfg')
    
        self.pathFilesGML = parser.get('Data',      'GMLfilesPath')
        self.mapServerURL = parser.get('MapServer', 'MapServerURL')
        self.mapFilesPath = parser.get('MapServer', 'mapFilesPath')
        self.mapTemplate  = parser.get('MapServer', 'mapTemplate')
        self.imagePath    = parser.get('MapServer', 'imagePath')
        self.imageURL     = parser.get('MapServer', 'imgeURL')
        self.otherProjs   = parser.get('MapServer', 'otherProjs')
        
    def buildRequest(self, serverAddress, processId, inputNames, inputValues):
        
        if len(inputNames) <> len(inputValues):
            print "Different number of input names and values."
            return
        
        inputs = ""
        for i in range(0, len(inputNames)):
            inputs += inputNames[i] + "=" + inputValues[i]
            if (i < (len(inputNames) - 1)):
                inputs += ";"
                
        self.request  = serverAddress
        self.request += "&REQUEST=Execute&IDENTIFIER=" + processId
        self.request += "&SERVICE=WPS&VERSION=1.0.0&DATAINPUTS=" + inputs
        
    def sendRequest(self):
        """ 
        At this stage this method works purely as download manager.
        Later on it will send a request on remote execution mode.
        It is inspired on this page:
        http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way/863017#863017
        """       
        
        self.buildRequest(serverAddress, processId, inputNames, inputValues)
        
        if(self.request == None):
            print "It wasn't possible to build a request with the given arguments"
            return

        print "Starting download of %s" %self.request
    
        r = urllib2.urlopen(urllib2.Request(self.request))
        self.xmlResponse = r.read()
        r.close()
        
        #Check if the process ran successfully
        if "<wps:ProcessFailed>" in self.xmlResponse:
            print "The remote process failed with the following message:\n"
            print self.xmlResponse.split("<ows:ProcessFailed>")[1].split("</ows:ProcessFailed>")[0] + "\n"
            return
    
        # Process the outputs
        outVector = self.xmlResponse.split("<wps:Output>")
        for o in outVector:
            if o.count("wps:LiteralData") > 0:
                self.resultsLiteral.append(LiteralOutput(o))
            elif o.count("wps:ComplexData") > 0:
                self.resultsComplex.append(ComplexOutput(o, self.UUID))
                                           
        # Save complex outputs to disk
        for c in self.resultsComplex:
            c.saveToDisk(self.pathFilesGML)
        
    def generateMapFile(self):
        
        map = UMN.MapFile(self.UUID)
        
        map.shapePath    = self.pathFilesGML
        map.epsgCode     = self.epsg
        map.mapTemplate  = self.mapTemplate
        map.imagePath    = self.imagePath
        map.imageURL     = self.imageURL
        map.mapServerURL = self.mapServerURL
        map.mapFilesPath = self.mapFilesPath
        map.otherProjs   = self.otherProjs
        
        for c in self.resultsComplex:
            style = UMN.MapStyle()
            layer = UMN.VectorLayer(c.path)
            layer.layerType = "Polygon"
            layer.addStyle(style)
            map.addLayer(layer)
        
        map.writeToDisk()
        
        
    
    