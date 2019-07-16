#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:39:38 2019

@author: opasina
"""

import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

onlyPlayerStats = pd.read_csv("NbaPlayerStats20172019.csv")





#salaries = onlyPlayerStats[onlyPlayerStats.columns[-2]]
#playerSeasonStats = onlyPlayerStats[onlyPlayerStats.columns[0:21]]

#onlyPlayerStats["Salary"] = onlyPlayerStats[onlyPlayerStats.columns[17:]].replace('[\$,]', '', regex=True).astype(float)

sns.heatmap(onlyPlayerStats.corr(), cmap="seismic", annot=True, vmin=-1, vmax=1);


onlyPlayerStatsNameIndex = onlyPlayerStats.set_index(["Name"] )

### Split data into X and Y

X, y = onlyPlayerStatsNameIndex.drop(['Salary'],axis=1), onlyPlayerStatsNameIndex['Salary']
X, X_test, y, y_test = train_test_split(X, y, test_size=.2, random_state=10)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.25, random_state=3)


lm = LinearRegression()

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train.values)
X_val_scaled = scaler.transform(X_val.values)
X_test_scaled = scaler.transform(X_test.values)

lm_reg = Ridge(alpha=1)

lm.fit(X_train, y_train)
print(f'Linear Regression val R^2: {lm.score(X_val, y_val):.3f}')

lm_reg.fit(X_train_scaled, y_train)
print(f'Ridge Regression val R^2: {lm_reg.score(X_val_scaled, y_val):.3f}')

lm.fit(X,y)
print(f'Linear Regression test R^2: {lm.score(X_test, y_test):.3f}')

y_pred = lm.predict(X_test)

