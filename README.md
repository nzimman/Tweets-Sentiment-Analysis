# Tweets Sentiment Analysis

## Synopsis
The goal of this project is to construct a data pipeline that analyzes the sentiment of tweets.

## Data Pipeline
![Screenshot](pipeline.png)


### Tweets Collector
For collecting tweets, one needs Twitter credentials (first  register the application on apps.twitter.com and create *Acces Tokens*). 

This part of the data flow consists of:
- config.py: contains Twitter credentials --> Need to add your own credentials
- twitter_streammer.py: handles authentication, listens live tweets, filters tweets by keyword and language, parses the tweets for relevant data and loads the data into MongoDB database.

### MongoDB


### ETL Job


### Sentiment Analysis


### PostGres


## Implementation: Docker


