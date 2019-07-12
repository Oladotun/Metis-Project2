# Metis-Project2
## REDEFINED PROJECT PROPOSAL, METIS PROJECT #2
## DOTUN OPASINA

## ITERATION:

Initially when I began this project, I proposed utilizing [sport injuries data to predict team sucess](https://github.com/Oladotun/Metis_Project_2_SportInjuries_TeamSucess) but on further evaluation and discussions with my advisors at Metis. We realized that it will be tough to create properly create such predictions and the current nba datasets on injuries is not large enough to provide meaningful results.

## ITERATIVE PROCESS:
On that note, I have decided to change my research question and predict the next season salaries of a basketball players based on their current season performace statistics. The problem lends itself easily to a linear regression solution and I can gather a lot of data on the subject.

## SCOPE:

The NBA Contract Signings for the 2019-2020 is currently going on. Many players are changing teams and others are renewing their contract. These moves by the players such as Kevin Durant, Kawhi Leonard, Kyrie Irving, and many more promises to make the next NBA 2019-2020 season an exciting one.

This excitement has led me to ask the questions : "Can we predict an NBA player Salaries based on their current season performance ?". This question can be used to evaluate the player's impact and in an industry whereby salaries are guaranteed to justify what the player should be worth in his next contract or team.

## METHODOLOGY:
1. Scrape Player Salary and Contract information data afrom Basketball Reference <br>
2. Scrape Player Sport Injuries data from specific seasons from Pro Sports Transactions<br>
3. Calculate Player [Player Efficiency Rating (PER)](https://www.basketball-reference.com/about/per.html) <br>
4. Build linear regression model using current scraped data<br>

## DATA SOURCES:
-  [Pro Sports Transactions ](http://www.prosportstransactions.com/basketball/) <br>
-  [Basketball Reference](https://www.basketball-reference.com/)

## TARGET
- MVP: Prediction of player salaries based on player statistics for seasons 2008 - 2012.
- Goal: Prediction of player salaries based on player statistics and whether or not they had an injury from 2008 - 2019.

## FEATURES
  - Player Name
  - Age Of Player
  - Height - Height in cm
  - Weight - Weight in lbs
  - Year - Year of Season
  - Team - Team of Player
  - Salary - Salary Offered for the Season
  - G - Games, The number of games a player or team played where a specified criteria occured
  - PER - PER: Player Efficiency Rating is the overall rating of a player's per-minute statistical production. The league average is 15.00 every season
  - FG - Field Goal
  - FGA - Field Goal Attempted
  - X3P - 3 Point Shots
  - FT - Free Throws
  - FTA - Free Throws Attempted
  - FT. - Free Throw Percentage; the formula is FT / FTA
  - ORB - Offensive Rebounds
  - DRB - Defensive Rebounds
  - TRB - Total Rebounds
  - AST - Assists
  - STL - Steals
  - BLK - Blocks
  - TOV - Turnovers
  - VOP - Value of Posession
  - Factor
  - PF - Personal Fouls
  - MPG - Minutes Per Game
  - lg_PTS - League Points
  - lg_FGA
  - lg_FG
  - lg_FT
  - lg_ORB
  - lg_TOV
  - lg_FTA
  - lg_FT
  - lg_FG
  - lg_TRB
  - lg_Pace
  - team_Pace
  - team_AST
  - team_FG

For more on the names chack the glossary [here](https://www.basketball-reference.com/about/glossary.html) 
## FEATURES TO INCLUDE INTO LINEAR REGRESSION MODEL
### X
- Player's name
- Age of Player
- Height of Player
- Weight of Player
- Number of Seasons played
- Player Efficiency Rating
- Player Injury report per season
### Y
- Player current Salary


## THINGS TO CONSIDER
- Scraping the data may take longer than expected.
- In terms of using Regression I need to make sure that the way I represent the team's record lends itself to the model.
- Calculating the PER is an extensive process and needs to be well thought out.

