# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 10:25:52 2015

@author: jserrano
"""
from __future__ import division
from yaml import safe_load
from datautils import Struct

__all__ = ["Struct","AbstractEstimator","MeaningCloudEstimator"]

class AbstractEstimator(object):
    def __init__(self,model=None):
        self._response = {}
        self._model = model
        
    def predict(self,response):
        pass
    
    def _process(self,*fields):
        # return ERROR if the field doesn't exist in _config and/or _response
        return tuple([self._parameters[field](self._response[field]) for field in fields])
  
    parameters = property(lambda self: self._parameters,None,None,"parameters")
    response = property(lambda self: self._response,None,None,"response")
    model = property(lambda self: self._model,None,None,"model to fit")

class MeaningCloudEstimator(AbstractEstimator):
    """ Fit a model to the response got from Meaning Cloud v 2.0 \n
        https://www.meaningcloud.com/developer/sentiment-analysis/doc/2.0/endpoint
        
        Arguments
        ---------
            model (confidence,score_tag,irony,agreement,subjectivity,*args):
                model to fit, args: model's parameters (by default, just one) 
    """
        
    def __init__(self,model=None):
        super(MeaningCloudEstimator,self).__init__(model)
        self._parameters  = Struct(**{\
                         "confidence":   lambda conf:  int(conf)/100,
                         "score_tag":    lambda tag:   {"P+":1,"P":.5,"NEU":0,"N":-.5,"N+":-1,"NONE":None}[tag],
                         "agreement":    lambda agree: {"AGREEMENT": 1, "DISAGREEMENT": -1}[agree],
                         "subjectivity": lambda obj:   {"OBJECTIVE": 1, "SUBJECTIVE": -1}[obj],
                         "irony":        lambda irony: {"NONIRONIC": 1, "IRONIC": -1}[irony],
                         "sigma": 0.1})
        if model is None:
            def model(conf,score,irony,agree,subjc,*args):
                return (1 + (agree+subjc)*args[0])*(conf*score*irony)
        self._model = model
        
    def predict(self,response):
        self._response.update(response)
        if self._process("score_tag") is None:
            return None
        else:
            sigma = self._parameters["sigma"]
            conf, score, irony, agree, subjc = \
                self._process("confidence","score_tag","irony","agreement","subjectivity")
            sentiment = self._model(conf,score,irony,agree,subjc,sigma)
        return sentiment
        
# "__main__", "__test__"
if __name__=="__test__":
    from analyzers import *
    config = Struct(**safe_load(open("meaningCloudConfig.json","r")))
    analyzer = MeaningCloudAnalyzer(config)
    r = analyzer.analyze("This product is awful\n I'm going to return it")
    o = MeaningCloudEstimator()
    o.predict(r)