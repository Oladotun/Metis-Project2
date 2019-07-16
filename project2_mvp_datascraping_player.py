#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 19:55:54 2019

@author: opasina
"""

from bs4 import BeautifulSoup
import pandas as pd

import requests
from selenium import webdriver



## Get request call
def requestCall(link):
    r  = requests.get("https://www.basketball-reference.com"+link)
    data = r.text
    soup = BeautifulSoup(data, "html")
    
    return soup

def seleniumCall(link):
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get('https://www.basketball-reference.com' + link)
    html = driver.page_source
    soup = BeautifulSoup(html)
    
    return soup
    
## Get Table
def getTable(requestLink,idRequest=[],pageType="static"):
#    print("I am going to get "+ requestLink)
    table = []
    if pageType == "static":
        soup = requestCall(requestLink)
    else:
        soup = seleniumCall(requestLink)
#    if soup != "":
#        print("soup not empty")
#    print(soup)
    
#    return soup
    for tagType in idRequest:
#        print(tagType)
        table.append(soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']==tagType))
    print(table)
    if len(table) == 0:
        print("We have a problem")
    return table

## Get Page Links    
def getPageLinks(requestLink,idRequest,startIndex,endIndex=0,pageType="static"):
    print(pageType)
    allTables = getTable(requestLink,idRequest,pageType)
    print(allTables)
    if len(allTables) > 0:
        for table in allTables:
            rows = table.findAll(lambda tag: tag.name=='tr')
            currStartIndex = startIndex
            currEndIndex = endIndex if endIndex > startIndex else len(rows)
            returnedLinks=[]
            for index in range(currStartIndex,currEndIndex):
                season = rows[index].find('a', href=True)
                if season.has_attr('href'):
                    returnedLinks.append(season['href'])
    return returnedLinks

seasonLinks =  getTable("/players/a/abrinal01.html",["advanced","all_salaries"],"dynamic")

view = pd.read_html(str(seasonLinks[0]))[0]


file = open("./testfile.html","w") 
 
file.write(str(seasonLinks) )

 
file.close() 
#getPageLinks("/leagues/NBA_2019_totals.html",["all_totals_stats"],0,0,"dynamic")






