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
#    print("I am going to get "+ requestLink)
    table = []
    if pageType == "static":
        soup = requestCall(requestLink)
    else:
        soup = seleniumCall(requestLink)
#    if soup != "":
#        print("soup not empty")
        
    for tagType in idRequest:
#        print(tagType)
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


eastWestZones = []
finalFrame = pd.DataFrame()
for season in range(0,3):
    eastLinks = getPageLinks(str(seasonLinks[season]),["confs_standings_E"],1) 
    westLinks = getPageLinks(str(seasonLinks[season]),["confs_standings_W"],1) 
    
    eastWestZones = eastWestZones + eastLinks + westLinks
    print("Season: "+ seasonLinks[season])
count = 0
seasonCount = 0
for zones in eastWestZones:  
    if count % 30 == 0 and count > 0:
        seasonCount = seasonCount + 1
    print("I am in team " + str(count + 1) + " We have "+ str(len(eastWestZones) + 1 ) + " to go");
    print("current zone is "+ zones)
    print("current season is" + seasonLinks[seasonCount])
    pergame_table = getTable(zones,["per_game","team_and_opponent","team_misc","salaries2"],"dynamic")
    
            
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
                                         "FTA","STL","BLK","PF","PTS/G"],axis=1)
    player_salaries = player_salaries.set_index('Name')
    
    ## Play Stats and Salaries Merged Together
    playStatsSalaries = neededPlayStats.merge(player_salaries, left_on='Name', right_on='Name')
    strSeasonLinks = seasonLinks[seasonCount]
    
    playStatsSalaries['Season'] = strSeasonLinks[-13:-5]
    playStatsSalaries['team_AST'] = team_needed_stats['AST']
    playStatsSalaries['team_Pace'] = team_needed_stats['Pace']
    playStatsSalaries['team_FG'] = team_needed_stats['FG']
    playStatsSalaries['team_Name'] = zones[7:10]
    
    
    
    '''
        Get League information for calculating PER 
    '''
    print("Current season to get league table is "+ strSeasonLinks)
    if count % 30 == 0:
        leagueMiscLink =  getTable(strSeasonLinks,["misc_stats","team-stats-per_game"],"dynamic")
        leaguePd = pd.read_html(str(leagueMiscLink[0]))[0]
        leagueStatsPd = pd.read_html(str(leagueMiscLink[1]))[0]
        
        lastValue = leaguePd.iloc[-1:]  # Get League Average
        lastValue.columns  = ['Rk','Team','Age','W','L','PW','PL','MOV','SOS','SRS','ORtg','DRtg','NRtg',
                           'Pace','FTr','3PAr','TS%','OF_eFG%','OF_TOV%','ORB%','OFF_FT/FGA',
                           'DF_eFG%','DF_TOV%','DRB%','DF_FT/FGA','Arena','Attend','Attendance/G']
        
        leaguePace = lastValue.reindex(["Pace"], axis = 1)
        averageLeagueStats = leagueStatsPd.iloc[-1:]
        averageLeagueStats.columns = ["lg_"+ str(stat) for stat in averageLeagueStats.columns ]
        
        ### Get Average League information
        needAverageLeagueStats = averageLeagueStats.reindex(["lg_FG"
                                             ,"lg_FT","lg_PF","lg_PTS","lg_AST","lg_FGA","lg_TOV","lg_ORB","lg_TRB",
                                             "lg_FTA"],axis=1)
        needAverageLeagueStats["lg_PPG"] = float(averageLeagueStats["lg_PTS"])/82 ### Points per game
        needAverageLeagueStats["lg_Pace"] = leaguePace["Pace"].values
    
    ## Update counter 
    '''
        Update the PlayStat with League information
    '''
    count = count + 1
    if len(needAverageLeagueStats) > 0 :
        for column in needAverageLeagueStats.columns:
            playStatsSalaries[column] =  needAverageLeagueStats[column].values[0]
    
    ### Add to the Final Frame for players
    finalFrame = finalFrame.append(playStatsSalaries)
    print("The total length of players are: ")
    print(len(finalFrame))
## Get final frame index
finalFrame = finalFrame.reset_index()
finalFrame.to_csv("./NbaPlayerStats20172019.csv",index=False)
 
    
