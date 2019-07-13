#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 04:34:37 2019

@author: opasina
"""

from bs4 import BeautifulSoup

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
def getTable(requestLink,idRequest,pageType="static"):
    if pageType == "static":
        soup = requestCall(requestLink)
    else:
        soup = seleniumCall(requestLink)
#    print(soup)
    table = soup.findAll(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']==idRequest)
#    print(table)
    return table

## Get Page Links    
def getPageLinks(requestLink,idRequest,startIndex,endIndex=0):
    table = getTable(requestLink,idRequest)
    if len(table) > 0:
        rows = table[0].findAll(lambda tag: tag.name=='tr')
        currStartIndex = startIndex
        currEndIndex = endIndex if endIndex > startIndex else len(rows)
        returnedLinks=[]
        for index in range(currStartIndex,currEndIndex):
            season = rows[index].find('a', href=True)
            if season.has_attr('href'):
                returnedLinks.append(season['href'])
    return returnedLinks
    
    
seasonLinks = getPageLinks("/leagues","stats",4,19)

for season in seasonLinks:
    eastLinks = getPageLinks(str(season),"confs_standings_E",1) 
    westLinks = getPageLinks(str(season),"confs_standings_W",1) 
    
pergame_table = getTable(eastLinks[0],"per_game","dynamic")

def printToHtml(name):
    with open(name+".html", 'w') as f:
        print(pergame_table, file=f)
        

#driver = webdriver.Chrome(executable_path='./chromedriver')
#driver.get('https://www.basketball-reference.com/teams/TOR/2018.html')
#
#html = driver.page_source
#soup = BeautifulSoup(html)



### Visit Leauges Page on Basketball reference    
#soup = requestCall("/leagues")
#
### Get Leagues table details
#table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="stats") 
#rows = table.findAll(lambda tag: tag.name=='tr')
#startIndex = 4 #Start at NBA Season 2018
#EndIndex = 19 # End at NBA Season 2004
#
### Get Season Links from 2004 - 2018 
#seasonLinks=[]
#for index in range(startIndex,EndIndex):
#    season = rows[index].find('a', href=True)
#    if season.has_attr('href'):
#        seasonLinks.append(season['href'])

## Get Teams 

#for seasonLink in seasonLinks:
#soup = requestCall(str(seasonLinks[0]))  
#table_E = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="confs_standings_E")
#E_Rows = table_E.findAll(lambda tag:tag.name=='tr')
#E_Rows[1].find('a', href=True)
#  
    
