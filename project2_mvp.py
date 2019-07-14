#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 04:34:37 2019

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
    table = []
    if pageType == "static":
        soup = requestCall(requestLink)
    else:
        soup = seleniumCall(requestLink)
    if soup != "":
        print("soup not empty")
        
    for tagType in idRequest:
        print(tagType)
        table.append(soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']==tagType))
#    print(table)
    if len(table) == 0:
        print("We have a problem")
    return table

## Get Page Links    
def getPageLinks(requestLink,idRequest,startIndex,endIndex=0):
    allTables = getTable(requestLink,idRequest)
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
    
    
seasonLinks = getPageLinks("/leagues",["stats"],3,19)

for season in seasonLinks:
    eastLinks = getPageLinks(str(seasonLinks[0]),["confs_standings_E"],1) 
    westLinks = getPageLinks(str(seasonLinks[0]),["confs_standings_W"],1) 
    
pergame_table = getTable(eastLinks[0],["per_game","team_and_opponent","team_misc","salaries2"],"dynamic")

        
playStats = pd.read_html(str(pergame_table[0]))[0]
team_opp_stats = pd.read_html(str(pergame_table[1]))[0]
team_misc_stats = pd.read_html(str(pergame_table[2]))[0]
player_salaries = pd.read_html(str(pergame_table[3]))[0]

playStats.columns = ['Rk_stats', 'Name', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS/G']
team_opp_stats.columns = ['SectionIndex', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P',
       '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL',
       'BLK', 'TOV', 'PF', 'PTS']
team_misc_stats.columns =  ['SECTION_INDEX','W','L','PW','PL', 'MOV','SOS', 'SRS','ORtg',
                            'DRtg','Pace','FTr', '3PAr','eFG_OFF%','TOV_OFF%','ORB_OFF%','FT/FGA_OFF',
                            'eFG_DEF%','TOV_DEF%','DRB_DEF%','FT/FGA_DEF',
                            'Arena','Attendance']
player_salaries.columns = ['Rk_salary', 'Name', 'Salary']

## Clean up Team misc and Team stats table 
team_misc_stats.set_index('SECTION_INDEX',inplace=True)
result_team = team_misc_stats.loc['Team'].reset_index().set_index("index")
result_team.loc['Pace'].values[0]

## Get Pace and append it to team stats
team_opp_stats = team_opp_stats.iloc[1,:]
sers = pd.Series({'Pace':result_team.loc['Pace'].values[0]})
team_opp_stats = team_opp_stats.append(sers)

### Output of Team info needed for PER
team_needed_stats = team_opp_stats[['AST','Pace','FG']]


## Player Stats Info
playStats = playStats.set_index('Name')
neededPlayStats = playStats.reindex(["Rk_stats","Age","MP","3P","AST","FG"
                                     ,"FT","TOV","DRB","FGA","TRB","ORB",
                                     "FTA","FT","STL","BLK","PF","PTS/G"],axis=1)
player_salaries = player_salaries.set_index('Name')

## Play Stats and Salaries Merged Together
playStatsSalaries = neededPlayStats.merge(player_salaries, left_on='Name', right_on='Name')
strSeasonLinks = seasonLinks[0]
playStatsSalaries['Season'] = strSeasonLinks[-13:-5]



'''
    Get League information for calculating PER 
'''



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
    
