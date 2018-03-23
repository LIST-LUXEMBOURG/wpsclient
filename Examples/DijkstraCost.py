# coding: utf-8
'''
Copyright 2010 - 2019 Luxembourg Institute of Science and Technology. 

Licenced under the EUPL, Version 1.1 or – as soon they will be approved by the
European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:

http://ec.europa.eu/idabc/eupl

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the Licence for the
specific language governing permissions and limitations under the Licence.

Created on Jan 17, 2014

@author: desousa
'''

from Example import Example
import WPSClient

class DijkstraCost(Example):

    def __init__(self):
    
        Example.__init__(self)
        
        self.outputs = {"path":"ShortestPathWithCost"}
        
        # Test with a WFS resource
        self.iniCli.init(
		    # Process Server address
		    #"http://wps.iguess.tudor.lu/cgi-bin/pywps-lamilo.cgi?", 
            "http://localhost/cgi-bin/pywps-lamilo.cgi?",
		    # Process name
		    "dijkstraCostSurface", 
		    # Inputs
		    [("cost_map", "http://iguess-mapserv.kirchberg.tudor.lu/cgi-bin/mapserv?map=/srv/mapserv/MapFiles/LUX_samples.map&SERVICE=WCS&FORMAT=image/img&BBOX=58830.138487593,61071.366931351,83970.452589199,85347.752713314&RESX=86.3928319642818&RESY=86.3928319642818&RESPONSE_CRS=EPSG:2169&CRS=EPSG:2169&VERSION=1.0.0&REQUEST=GetCoverage&COVERAGE=LuxProtectedAreas"), 
             ('start_latitude', '49.520821'),
             ('target_latitude', '49.611'),
             ('start_longitude', '6.006353'),
             ('target_longitude', '6.129')],
		    # Outputs
		    self.outputs)
        
        
