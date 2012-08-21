import os, sys, shutil, urllib2, urlparse
from array import array

###########################################################

def splitComplexOutputs(outputs):
	
	results = []
	compData = outputs.split("<wps:ComplexData>")
	compData.remove(compData[0])

	for r in compData:
		x = r.split("</wps:ComplexData>")
		print x
		results.append(x[0])
	return results

###########################################################

def saveOutputsGML(dest, fileName, outputList):

	i = 1
	for out in outputList:

		try:
			fileName = os.path.join(dest, fileName + "_" + str(i) + ".gml")
			with open(fileName, 'wb') as f:
				f.write(out)

		finally:
			f.close()

		print "Saved in %s" %fileName
		i = i + 1;

###########################################################


def download(url, dest, fileName=None):

#based on: 

#http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way/863017#863017

    print "Start downloading of %s" %url

    r = urllib2.urlopen(urllib2.Request(url))

    print "--------------------------"
    res = splitComplexOutputs(r.read())
    saveOutputsGML(dest, fileName, res)
    print "--------------------------"

    try:

        fileName = os.path.join(dest, fileName)

        with open(fileName, 'wb') as f:

            shutil.copyfileobj(r,f)

        print "Saved in %s" %fileName

    finally:

        r.close()

## Test the split function
print "################"
s = "IIIII<wps:ComplexData>AA</wps:ComplexData>XX<wps:ComplexData>BB</wps:ComplexData>XX"
r = splitComplexOutputs(s)
for i in r:
	print i
print "################"



wfsfile = "test2"
path2save2 = ""
wfsurl = "http://iguess.tudor.lu/cgi-bin/pywps.cgi?&REQUEST=Execute&IDENTIFIER=ogrbuffer&SERVICE=WPS&VERSION=1.0.0&DATAINPUTS=size=1;data=http%3A%2F%2Figuess.tudor.lu%2Fpywps%2FsampleData%2FsampleLineRotterdam.xml"
download(wfsurl,path2save2 ,wfsfile)
