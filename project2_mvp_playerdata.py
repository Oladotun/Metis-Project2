#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:39:38 2019

@author: opasina
"""

import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plot
from sklearn.preprocessing import StandardScaler
import numpy as np
import math


### return split functions

def split_and_validate(X,y,test=.25,random=3):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test, random_state=random)
    
    # fit linear regression to training data
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    # score fit model on validation data
    val_score = lr_model.score(X_val, y_val)
    
    y_pred = lr_model.predict(X_val)

    residuals = y_val - y_pred
    

    # report results
    print('\nValidation R^2 score was:', val_score)
    print('Feature coefficient results:')
    for feature, coef in zip(X.columns, lr_model.coef_):
        print(feature, ':', f'{coef:.2f}')
    
    return X_train, X_val, y_train, y_val, residuals, lr_model


onlyPlayerStats = pd.read_csv("NbaPlayerStats20172019.csv")

#onlyPlayerStats =  onlyPlayerStats.drop(['Salary_Log','Salary_Log_predict'],axis=1)
#
#onlyPlayerStats.to_csv("NbaPlayerStats20172019.csv",index=False)

onlyPlayerStats = onlyPlayerStats.rename(columns={'3P' : 'ThreePoints', 'PTS/G': 'PointsPerGame' })


onlyPlayerStats.describe()

## Divide Minutes Played per game across all stats
#onlyPlayerStats[['MP', 'ThreePoints', 'AST', 'FG', 'FT', 'TOV', 'DRB','FGA', 'TRB', 'ORB', 'FTA', 'STL', 'BLK', 'PF', 'PointsPerGame']] = onlyPlayerStats[['MP', 'ThreePoints', 'AST', 'FG', 'FT', 'TOV', 'DRB','FGA', 'TRB', 'ORB', 'FTA', 'STL', 'BLK', 'PF', 'PointsPerGame']].div(onlyPlayerStats['MP'].astype(float),axis=0)


### Remove Player Salaries that are Zero 
onlyPlayerStats.drop(onlyPlayerStats[onlyPlayerStats.Salary == 0].index, inplace=True)

onlyPlayerStats["Salary_Log"] = np.log(onlyPlayerStats["Salary"])


### Find the best Lasso Score

X, y = onlyPlayerStats.drop(['Name','Salary', 'Salary_Log','Season'],axis=1), onlyPlayerStats['Salary_Log']

X_train, X_val, y_train, y_val, residuals, model = split_and_validate(X,y)

## Generate Lasso Initially 
std = StandardScaler()
std.fit(X_train.values)

X_tr = std.transform(X_train.values)
X_te = std.transform(X_val.values)


lassocv = LassoCV(cv=5, random_state=0)
lassocv.fit(X_tr, y_train)
lassocv.score(X_te, y_val)

## Plot out the Lasso Alphas
plot.plot(np.log10(lassocv.alphas_),lassocv.mse_path_)
plot.ylabel("Mean Squared Error")
plot.xlabel("Alpha (log10)")

columnList = list(zip(X.columns,lassocv.coef_))

print(columnList)

usefulColumns = [x[0] for x in columnList if x[1] != 0.0]

k = 4
plot.scatter(X_val.iloc[:,k],residuals, color = 'blue')
plot.xlabel(X_val.columns[k]) 
plot.ylabel('Residual')
plot.show()


## Column to Use for correlation table 

X, y = onlyPlayerStats[usefulColumns], onlyPlayerStats['Salary_Log']
usefulColumns.append('Salary_Log')
onlyUsefulColumns = onlyPlayerStats[usefulColumns]

snsPlot = sns.heatmap(onlyUsefulColumns.corr(), xticklabels=['Age', 'Minutes Played', 'Defensive Rebound', 'Fouls', 'Points', 'Log of Salary'], yticklabels=['Age', 'Minutes Played', 'Defensive Rebound', 'Fouls', 'Points', 'Log of Salary'],cmap="seismic", annot=True, vmin=-1, vmax=1)

snsPlot.set_xticklabels(snsPlot.get_xticklabels(), rotation = 0)

## Now work with Generated Lasso Result

X_train, X_val, y_train, y_val, residuals, model = split_and_validate(X,y) ## Generated new Scores

y_pred = model.predict(X)

onlyPlayerStats["Salary_Log_predict"] = y_pred

### Sort by Players


def getDataStatsSalary(onlyPlayerStats,usefulColumns,playerName):
    sortByPlayerStats = onlyPlayerStats.sort_values(by=['Name','Season'])

    ### Get Players, and Important Columns
    #usefulColumns.append("Salary")
    #usefulColumns.append("Salary_Log_predict")
    usefulColumns = ["Name"] + usefulColumns[0:5] + ["Season","Salary"] + [usefulColumns[5]] + ["Salary_Log_predict"]

    importedColumnSortedPlayers = sortByPlayerStats[usefulColumns]

    GiannisHistory = importedColumnSortedPlayers [importedColumnSortedPlayers["Name"] == playerName]

    arrayIndex = []
    for res in GiannisHistory["Salary_Log_predict"]:
#        print(math.exp(res))
        arrayIndex.append(math.exp(res))
    
    GiannisHistory["Salary_predicted"] = arrayIndex
    
    CompareData = GiannisHistory.drop(columns=["Salary_Log_predict", "Salary_Log"])
    
    return CompareData

 ## TestPlayers
playerComparedStatsJimmy = getDataStatsSalary(onlyPlayerStats,usefulColumns,"Jimmy Butler")
playerComparedStatsVictor = getDataStatsSalary(onlyPlayerStats,usefulColumns,"Victor Oladipo")
playerComparedStatsGiannis = getDataStatsSalary(onlyPlayerStats,usefulColumns,"Giannis Antetokounmpo")
playerComparedStatsPascal = getDataStatsSalary(onlyPlayerStats,usefulColumns,"Pascal Siakam")






