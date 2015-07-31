# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:01:25 2015

@author: jserrano
"""

from parsers import BloombergNewsParser

__all__ = ['GeneralNew']

class AbstractNew(object):

    def __init__(self,parser):
        self._parser = parser
    
    def __getitem__(self,name):
        return self.__dict__[name]
        
    def __str__(self):
        return self._struct.__repr__()

class GeneralNew(AbstractNew):

    def __init__(self,parser):
        super(GeneralNew,self).__init__(parser)
        self._struct = {"_id": None,
                        "source_id": None,
                        "entity_id": None,
                        "url": None,
                        "headline": None,
                        "authors": None,
                        "date": None,
                        "timezone": None,
                        "topics": None,
                        "body": None,
                        "body_struct": None}
        _dict = self._parser.parse(self._parser.read())
        D = {k: _dict[k] for k in self._struct.keys() if k in _dict.keys()}
        self._struct.update(D)
        self.__dict__.update(self._struct)

if __name__=="__main__":
    url = 'http://www.bloomberg.com/news/articles/2014-04-24/hungary-bonds-rally-as-forint-drops-on-central-bank-deposit-ban'
    r = BloombergNewsParser(url,165818,1,34)    
    n = GeneralNew(r)
    print n