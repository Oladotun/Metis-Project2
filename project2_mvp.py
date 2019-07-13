#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 04:34:37 2019

@author: opasina
"""

from bs4 import BeautifulSoup

import requests

## Get request call
def requestCall(link):
    r  = requests.get("https://www.basketball-reference.com"+link)
    data = r.text
    soup = BeautifulSoup(data, "html")
    
    return soup
    
soup = requestCall("/leagues")

## Get table details
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="stats") 
rows = table.findAll(lambda tag: tag.name=='tr')
startIndex = 4 # NBA Season 2018
EndIndex = 19 # NBA Season 2004

## Get Season Links 
seasonLinks=[]
for index in range(startIndex,EndIndex):
    season = rows[index].find('a', href=True)
    seasonLinks.append(season['href'])
    
