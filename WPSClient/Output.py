'''
Created on Sep 26, 2012

@author: desousa
'''

import os
import urllib2
import WPSTags.WPSTags as Tags

###########################################################

class Output:
    
    name = None
    value = None
    
    def __init__(self, rawString):
        
        self.name = rawString.split(Tags.preId)[1].split(Tags.sufId)[0]
        
    
    def getReferenceValue(self, rawString):
        
        if not (Tags.preRef in rawString):
            print "Error: tried to download a non reference output."
            return;
        
        url = rawString.split("wps:Reference href=\"")[1].split("\"")[0]
        r = urllib2.urlopen(urllib2.Request(url))
        self.value = r.read()
        r.close()
        

###########################################################

class LiteralOutput(Output):

    def __init__(self, rawString):

        Output.__init__(self, rawString)
        
        # If the data is included in the string itself
        if Tags.preLit in rawString:
            self.value = rawString.split(Tags.preLit)[1].split(">")[1].split(Tags.sufLit)[0].split("</wps:LiteralData")[0] 

        # Otherwise it is a reference
        else:
            self.getReferenceValue(rawString)

###########################################################

class ComplexOutput(Output):

    uniqueID = None
    path = None
    extension = "gml"

    def __init__(self, rawString, unique):

        Output.__init__(self, rawString)
        self.uniqueID = unique
        
        # If the data is included in the string itself
        if Tags.preCplx in rawString:
            
            self.value = rawString.split(Tags.preCplx)[1].split(Tags.sufCplx)[0]
            while self.value[0] <> "<":
                self.value = self.value[1:len(self.value)]
        
        # Otherwise it is a reference
        else:
            
            self.extension = rawString.split("mimeType=\"")[1].split("/")[1].split("\"")[0]
            self.getReferenceValue(rawString)
            

    def saveToDisk(self, dest):
        
        file = None
        self.path = os.path.join(dest, self.uniqueID + "_" + self.name + "." + self.extension)
        
        try:
            file = open(self.path, 'w')
            file.write(self.value)
            print "Saved output file: %s\n" %self.path
        except Exception, err:
            print "Error saving %s:\n%s" %(self.path, err)
        finally:
            if file <> None:
                file.close()
