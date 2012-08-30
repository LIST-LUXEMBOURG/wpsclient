'''
Created on Aug 9, 2012

@author: Luis de Sousa [luis.desousa@tudor.lu]

This file contains classes that serve as wrappers for the several components of
a MapServer mapfile. It can produce a sample mafile with a single layer if no 
arguments are passed to the constructors. 

Issues:
. Replace SHAPEPATH for direct links in the Layer class
. Makes sense to have initialisers in constructors?
. No support for raster layers.
. No support for PostGis layers. 

'''

mapscript=False
try:
    from mapscript import *
    mapscript=True
except Exception,e:
    print "MapScript could not be loaded, mapserver not supported: %s"

class MapFile:
    """ This class wraps up a MapServer map file containing vector data.
        The layers exposed are provided through both the WMS and WFS stadards """

    name            = None 
    bBox            = (91979, 436326, 92617, 437659.5)
#   minX            = "91979" 
#   minY            = "436326" 
#   maxX            = "92617"
#   maxY            = "437659.5" 
    shapePath       = "/home/desousa/Tudor/MUSIC/Rotterdam"
    epsgCode        = "28992"
    serviceTitle    = " A test service for the city of Rotterdam"
    mapTemplate     = "/var/www/MapServ/map.html"
    imagePath       = "/var/www/MapServ/map_images/"
    imageURL        = "/MapServ/map_images/"
    mapServerURL    = "http://localhost/cgi-bin/mapserv?map="
    mapFilesPath    = "/var/www/MapServ/"
    otherProjs      = "EPSG:3035 EPSG:4326 EPSG:3785 EPSG:900913"
    layers              = []

    def __init__(self, nameInit = "TestMapFile"):
        
        self.name = nameInit 
        # self.mapHeader()

    def mapHeader(self):

        text  = "MAP \n"
        text += "  NAME        \"" + self.name + "\"\n"
        text += "  IMAGETYPE   PNG \n"
        text += "  EXTENT      " + str(self.bBox[0]) + " " + str(self.bBox[1]) + " " + str(self.bBox[2]) + " " + str(self.bBox[3]) + "\n"
        text += "  SIZE        400 300 \n"
        text += "  SHAPEPATH   \"" + self.shapePath + "\"\n"
        text += "  IMAGECOLOR  255 255 255 \n"
        text += "  PROJECTION \n"
        text += "   \"init=epsg:" + self.epsgCode + "\"\n"
        text += "  END \n\n"

        text += "WEB \n"
        text += "  TEMPLATE  \"" + self.mapTemplate + "\"\n"
        text += "  IMAGEPATH \"" + self.imagePath + "\"\n"
        text += "  IMAGEURL  \"" + self.imageURL + "\"\n"
        text += "  METADATA \n"
        text += "    \"ows_title\"           \"" + self.serviceTitle + "\"\n"
        text += "    \"ows_onlineresource\" \"" + self.mapServerURL + self.filePath() + "&\"\n"
        text += "    \"ows_srs\"             \"EPSG:" + self.epsgCode + " " + self.otherProjs + "\"\n"
        text += "    \"ows_bbox_extended\" \"true\"\n"
        text += "    \"ows_enable_request\" \"*\"\n\n" 

        text += "  END  # Metadata\n\n"
        text += "END  # Web\n\n"

        text += "# Start of LAYER DEFINITIONS ---------------------------------\n\n"

        return text

    def mapFooter(self):

        text  = "  # End of LAYER DEFINITIONS -------------------------------\n"
        text += "END "

        return text

    def filePath(self):

        return self.mapFilesPath + self.name + ".map"


    def addLayer(self, layer):

        self.layers.append(layer)


    def getString(self):

        result = self.mapHeader()
        # If no layer has been declared add default layer
        if len(self.layers) <= 0:
            result += VectorLayer().getString()
        else:
            for layer in self.layers:
                result += layer.getString()
        result += self.mapFooter()

        return result

    def writeToDisk(self):
        FILE = open(self.filePath(),"w")
        FILE.write(self.getString())
        FILE.close()


###########################################################################3

class VectorLayer:
    """ Wrapper for the layer component of a MapServer mapfile.
        At this stage it supports vector layers."""

    name         = None
    layerType    = "POLYGON"
    title        = "A test layer"
    path         = None
    styles       = []

    def __init__(self, path, nameInit = "TestLayer"):
        
        self.path = path
        self.name = nameInit
        # self.LayerHeader()

    def layerHeader(self):

        text  = "  LAYER # " + self.name + " " + self.layerType + " ------------------------\n\n"
        text += "    NAME           " + self.name + "\n"
        text += "    CONNECTIONTYPE OGR\n"
        text += "    CONNECTION     \"" + self.path + "\"\n"
        #text += "    DATA         " + self.name + "\n"
        text += "    STATUS         OFF \n"
        text += "    TYPE           " + self.layerType + "\n"

        text += "  METADATA \n"
        text += "    \"DESCRIPTION\" \"" + self.name + "\"\n"
        text += "    \"ows_title\"   \"" + self.name + "\"\n"
        text += "  END  # Metadata \n\n"

        text += "    CLASS \n"
        text += "      NAME       \"" + self.title + "\"\n"

        return text


    def layerFooter(self):

        text  = "    END \n"
        text += "  END #" + self.name + " " + self.layerType + " ------------------------\n\n"
        return text


    def addStyle(self, style):

        self.styles.append(style)


    def getString(self):

        result = self.layerHeader()
        # If no style has been declared add default style
        if len(self.styles) <= 0:
            result += MapStyle().getString()
        else: 
            for style in self.styles:
                result += style.getString()
        result += self.layerFooter()

        return result
    

##############################################################################

class MapStyle:
    """ Wrapper for the MapServer style component of a vector layer. """

    penWidth = "2"
    colour = "220 100 100"

    def __init__(self, pen = "2", col = "160 0 0"):

        self.penWidth = pen
        self.colour = col
    
    def setColour(self, col):

        self.colour = col

    def setPen(self, pen):

        self.penWidth = pen

    def getString(self):

        text  = "      STYLE \n"
        text += "        COLOR        " + self.colour + "\n"
        text += "        WIDTH        " + self.penWidth + "\n"
        text += "        ANTIALIAS    TRUE \n"
        text += "      END \n"

        return text
        
