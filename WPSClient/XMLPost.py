'''
Created on Sep 26, 2012

@author: desousa
'''

import urllib2

class XMLPost:
    
    inputs = []
    outputs = []
    procName = None
    
    def __init__(self, procName):
        
        self.procName = procName
        
    def getHeader(self):
        
        s  = "<wps:Execute service=\"WPS\" version=\"1.0.0\" \n"
        s += " xmlns:wps=\"http://www.opengis.net/wps/1.0.0\" \n"
        s += " xmlns:ows=\"http://www.opengis.net/ows/1.1\" \n"
        s += " xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n"
        s += " xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" \n"
        s += " xsi:schemaLocation=\"http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd\">\n"
        s += " <ows:Identifier>" + self.procName + "</ows:Identifier>\n"
        return s
        
    def addRefInput(self, name, address):
        
        s  = "  <wps:Input>\n"
        s += "   <ows:Identifier>" + name + "</ows:Identifier>\n"
        s += "   <wps:Reference xlink:href=\"" + address + "\"/>\n"
        s += "  </wps:Input>\n"
        self.inputs.append(s)
        
    def addLiteralInput(self, name, value):
        
        s  = "  <wps:Input>\n"
        s += "   <ows:Identifier>" + name + "</ows:Identifier>\n"
        s += "   <wps:Data>\n"
        s += "    <wps:LiteralData>" + value + "</wps:LiteralData>\n"
        s += "   </wps:Data>\n"
        s += "  </wps:Input>\n"
        self.inputs.append(s)
        
    def addOutput(self, name):
        
        s  = "   <wps:Output asReference=\"true\">\n"
        s += "    <ows:Identifier>" + name + "</ows:Identifier>\n"
        s += "   </wps:Output>\n"
        self.outputs.append(s)
        
    def getFooter(self):
        
        s  = " <wps:ResponseForm>\n"
        s += "  <wps:ResponseDocument storeExecuteResponse=\"true\" status=\"true\">\n"
        for o in self.outputs:
            s += o
        s += "  </wps:ResponseDocument>\n"
        s += " </wps:ResponseForm>\n"
        s += "</wps:Execute>\n"
        return s
        
    def getString(self):
        
        s = self.getHeader()
        s += " <wps:DataInputs>\n"
        for i in self.inputs:
            s += i
        s += " </wps:DataInputs>\n"
        s += self.getFooter()
        return s
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        