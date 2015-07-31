# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:35:35 2015

@author: jserrano
"""
import numpy as np
import pandas as pd
import datetime as dt
from urllib2 import urlopen
from bs4 import BeautifulSoup as bs

query_url = lambda x,pag=1: 'http://www.bloomberg.com/search?query={}&category=Articles&page={}'.format(x,pag)
section = '.content-stories'
_id = 0

def get_articles(name='Telefonica'):
    count_articles = int(bs(urlopen(query_url(name,1)).read()).select(".search-category-facet .active")[1].text)
    maxpag = int(np.ceil(1+count_articles/10.))
    documents = []
    for pag in xrange(1,maxpag):
        documents += bs(urlopen(query_url(name,pag)).read()).select(section+' article')
    return documents
    
if __name__=="__main__":
    l = get_articles('Vodafone')
    elements,id_error = [],[]
    convert_ts = lambda e: dt.datetime.strptime(e,'%Y-%m-%dT%H:%M:%S+00:00')
    for i,element in enumerate(l):
        try:
            elements += [{"_id": _id,
                        "entity_id": 1,
                        "source_id": 1,
                        "topic": element.select('.metadata-topic')[0].attrs['href'],
                        "date": convert_ts(element.select('time')[0].attrs['datetime']),
                        "url": element.select('a')[-1].attrs['href']}]
            _id+=1
        except:
            id_error += [i]
    dates = pd.Series(np.sort([x['date'] for x in elements]))
    data = [x['date'] for x in elements]
    data = pd.Series(map(dt.timedelta.total_seconds,np.diff(np.sort(data))))/(60.*60.*24)    
    stats = data.describe(percentiles=[.05,.25,.50,.75,.99])
    data[data < stats['std']*3].plot(kind='kde',xlim=[0,40],title='days')
