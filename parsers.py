# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:46:07 2015

@author: jserrano
"""
import re
from urllib2 import urlopen
from bs4 import BeautifulSoup as bs

__all__ = ['GeneralParser','BloombergNewsParser']

class GeneralParser(object):    
    def parse(self,document):
        return {}

class BloombergNewsParser(GeneralParser):

    def __init__(self,url=None,_id=None,source_id=None,entity_id=None):
        self._url = url
        self._struct = {"_id": _id,
                "source_id": source_id,
                "entity_id": entity_id,
                "url": url,
                "headline": None,
                "authors": None,
                "date": None,
                "timezone": None,
                "topics": None,
                "body": None,
                "body_struct": None}
                
    def read(self):
        if not self._url is None:
            return urlopen(self._url).read()
    
    def parse(self,document=None):
        if not document is None:
            doc = bs(document)
            
            get_text = lambda y: map(lambda x: x.text, y)
            rm_seconds = lambda x: x.replace(re.findall('\.[0-9]*$',x)[0],'')
            rm_timezone = lambda x: x.replace(re.findall('[A-Z]*$',x)[0],'')
            
            # date:
            date = doc.select('time')[0].get('datetime') 
            # headers:
            H = {'h'+str(i): get_text(doc.select('.article-body__content h'+str(i))) for i in xrange(6)}
            # paragraphs:
            P = {'p': get_text(doc.select('.article-body__content p'))}  
            H.update(P)
            
            self._struct['headline'] = doc.select('#content h1')[0].text
            self._struct['authors']  = get_text(doc.select('.author-link'))
            self._struct['date']     = rm_seconds(rm_timezone(date)).replace('T',' ')
            self._struct['timezone'] = re.findall('[A-Z]*$',date)[0]            
            self._struct['topics']   = get_text(doc.select('.topic-list li'))
            self._struct['body']     = H
            self._struct['body_struct'] = filter(lambda y: not y is None, map(lambda x: x.name, doc.select('.article-body__content')[0].contents))
            return self._struct
        return self._struct