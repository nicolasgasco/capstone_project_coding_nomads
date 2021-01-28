# Python Twitter Analyzer
## [CodingNomads](https://codingnomads.co/) final project using tweepy and sqlalchemy

---
This is the final project of the online [Python course](https://codingnomads.co/courses/python-bootcamp-online/) by CodingNomads.

### Aim
The aim of the project is providing a series of statistics (e.g. average user count or most popular times) on a set of Twitter tweets fetched using *tweepy* and stored in a database using *sqlalchemy*.
The results of said statistics can be previewed in the three .txt files in the main folder of the project:
	- results_text_analysis.txt: stats on the text of the tweets, e.g. most frequently used symbols and longest word in the set.
	- results_time_analysis.txt: stats on the time when the tweets were written, e.g. most popular hours or oldest tweet.
	- results_users_analysis.txt: stats on the users, e.g. users with most followers or average followers/followed accounts ratio
	
### Description
The project consists of a series of scripts aimed at:
1. Use tweepy to fetch a list of users who recently wrote a tweet in English containing the word "cyberpunk". This was done to push the set of tweets towards the gaming world.
2. Use tweepy to fetch the last 20 tweets published by said users. Only tweets in English and that are not retweets of other tweets were accepted.
3. Use sqlalchemy to store and retrieve all the data in a database.
4. Use python scripts to analyze the collected data (one file where the results are printed and written in a .txt file and another with all the actual functions used).
