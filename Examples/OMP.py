# coding: utf-8
'''
Copyright 2010 - 2015 CRP Henri Tudor

Licenced under the EUPL, Version 1.1 or – as soon they will be approved by the
European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:

http://ec.europa.eu/idabc/eupl

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the Licence for the
specific language governing permissions and limitations under the Licence.

Created on Jan 20, 2015

@author: desousa
'''

from Example import Example
import WPSClient

class OMP(Example):

    def __init__(self):
    
        Example.__init__(self)
        
        self.outputs = {"omp_paths":"OMP_Paths"}
        
        # Test with a WFS resource
        self.iniCli.init(
            # Process Server address
            "http://wps.iguess.tudor.lu/cgi-bin/pywps-lamilo.cgi?", 
            #"http://localhost/cgi-bin/pywps-lamilo.cgi?",
            # Process name
            "omp", 
            # Inputs
            [("pois", "http://iguess-wps.kirchberg.tudor.lu/pywps/sampleData/luxembourg/LuxPOIs_4326.gml")],
            # Outputs
            self.outputs)
        
        
        