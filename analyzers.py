# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 08:46:54 2015

@author: jserrano
"""

from yaml import safe_load
from requests import post
from datautils import Struct

__all__ = ["Struct","AbstractAnalyzer","MeaningCloudAnalyzer"]

class AbstractAnalyzer(object):
    def __init__(self,config):
        self._config = config
        self._parameters = {"src": "sdk-python-2.0"}
        
    def analyze(self,text):
        pass
    
    config = property(lambda self: self._config,None,None,"Analyzer's config")    
    parameters = property(lambda self: self._parameters,None,None,"API's config")    

class MeaningCloudAnalyzer(AbstractAnalyzer):
    def __init__(self,config):
        super(MeaningCloudAnalyzer,self).__init__(config)
        self._parameters.update(self._config.__dict__)
    
    def analyze(self,text):
        self._parameters["txt"] = text
        response = post(self._config.api, params=self._parameters).content
        return safe_load(response)
        
if __name__=="__main__":
    config = Struct(**safe_load(open("meaningCloudConfig.json","r")))
    analyzer = MeaningCloudAnalyzer(config)
    r = analyzer.analyze("This product is awful")
    