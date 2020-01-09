from pymongo import MongoClient
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
import time as t
from datetime import datetime, timedelta
import numpy as np

# Wait 5 minutes
t.sleep(300)

# Connect to MongoDB
mongoClient = MongoClient('mongodb_pipe')
db = mongoClient.twitter_data
collection = db.tweets2

# Connect to postgres
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'postgresdb_pipe' #127.0.0.1 --> IP address loop back
PORT = '5432'
DBNAME = 'tweets'

# connection string
conn_string = f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
db = create_engine(conn_string)

# For the Sentiment analysis
analyser = SentimentIntensityAnalyzer()
# Sentiment analysis function
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score


for i in range(10):
    print('\n')
    print(f'round: {i}')
    print('\n')

    endtime = datetime.now()
    starttime = endtime + timedelta(minutes = -5)

    endtime_t = np.double(datetime.timestamp(endtime))
    starttime_t = np.double(datetime.timestamp(starttime))

    print(endtime_t)
    print(starttime_t)

    # Initialize df
    df = pd.DataFrame()

    # Look for tweets in MongoDB
    details = collection.find()

    for x in details:
        if (np.double(x['timestamp']) > starttime_t) and (np.double(x['timestamp']) <= endtime_t):
            #Create a df with existing tweet data
            lst = [[x['date_stamp'],x['timestamp'],x['user'],x['clean_text']]]
            df1 = pd.DataFrame(lst, columns =['date_tweet','timestp', 'User','Text'])
            #Do sentiment analysis on the clean Text
            result = sentiment_analyzer_scores(x['clean_text'])

            df1['neg']=result['neg']
            df1['neu']=result['neu']
            df1['pos']=result['pos']
            df1['compound']=result['compound']
            df = df.append(df1)

    df.to_sql('tweet_imp', db, index=False, if_exists="append")

    t.sleep(300)
