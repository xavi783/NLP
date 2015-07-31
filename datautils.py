# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:46:48 2015

@author: jserrano
"""

import json

__all__ = ['Struct']

class Struct(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
    
    def __getitem__(self,name):
        return self.__dict__[name]
        
    def __str__(self):
        return self.__dict__.__repr__()

if __name__=='__main__':
    c = Struct(**json.load(open('amazonkeys.json','r')))