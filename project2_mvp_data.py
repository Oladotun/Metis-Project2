#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:12:55 2019

@author: opasina
"""

import pandas as pd

playerStats = pd.read_csv("NbaPlayerStats20172019.csv")

### Do needed calculation for Player Rating

playerStats["DRB%"] = (playerStats["lg_TRB"] - playerStats["lg_ORB"]).astype(float) / (playerStats["lg_TRB"]).astype(float)
playerStats["VOP"] = (playerStats["lg_PTS"]).astype(float)/(playerStats["lg_FGA"] - playerStats["lg_ORB"] + playerStats["lg_TOV"] +(0.44 * playerStats["lg_FTA"])).astype(float)
playerStats["factor"] = (2.0 / 3.0) - (0.5 * ((playerStats["lg_AST"]).astype(float)/ (playerStats["lg_FG"]).astype(float))) / (2 * ((playerStats["lg_FG"]).astype(float) / (playerStats["lg_FT"]).astype(float)))

#U player efficiency rating

iMP = (1/(playerStats["MP"]).astype(float))
teamASTFG = (playerStats["team_AST"]).astype(float)/(playerStats["team_FG"]).astype(float)
AddPart = ((playerStats["3P"]).astype(float) + 
           ((2.0/3.0) * (playerStats["AST"]).astype(float)) +
           (2 - playerStats["factor"] * (teamASTFG *playerStats["FG"] ) +
           (playerStats["FG"].astype(float) * 
            0.5 * (1 + (1 - teamASTFG) + (2.0/3.0 * teamASTFG)))
           
            - (playerStats["VOP"] * playerStats["TOV"])
            - (playerStats["VOP"] * playerStats["DRB%"] * (playerStats["FGA"]-playerStats["FG"]))
            - (playerStats["VOP"] * 0.44 * (0.44 + (0.56 * playerStats["DRB%"])) * (playerStats["FTA"]-playerStats["FT"]))
            + (playerStats["VOP"] * (1 - playerStats["DRB%"]) * (playerStats["TRB"]- playerStats["ORB"]))
            + (playerStats["VOP"] * (playerStats["DRB%"]) * (playerStats["ORB"]))
            + (playerStats["VOP"] * (playerStats["STL"]) 
            + (playerStats["VOP"] * (playerStats["DRB%"]) * (playerStats["BLK"]))
            - (playerStats["PF"] * ((playerStats["lg_FT"]).astype(float)/(playerStats["lg_PF"]).astype(float)) 
            - (0.44 
               * ((playerStats["lg_FTA"]).astype(float)/(playerStats["lg_PF"]).astype(float))) 
                * (playerStats["VOP"]).astype(float))
                     
            )))
            
uper = iMP * AddPart

pace_adj = playerStats["lg_Pace"] / playerStats["team_Pace"]

a_per = pace_adj * uper

PER = a_per * 15.0

playerStats["per"] = PER

playerStats = playerStats.drop(columns=['FT.1'])
per_form = ( (playerStats["FG"] * 85.910)
              + (playerStats["STL"] * 53.897)
              + (playerStats["3P"] * 51.757)
              + (playerStats["FT"] * 46.845)
              + (playerStats["BLK"] * 39.190)
              + (playerStats["ORB"] * 39.190)
              + (playerStats["AST"] * 34.677)
              + (playerStats["DRB"] * 14.707)
              - (playerStats["PF"] * 17.174)
              - (3.5 * 20.091)  
              - (playerStats["TOV"] * 53.897) 
        ) * iMP

playerStats["per"] = per_form
## Weighted PER 

