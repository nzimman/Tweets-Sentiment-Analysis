from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import pandas as pd
import pymongo
import urllib.parse
import datetime
from config import cfg

HOST = 'localhost'
PORT = '27017' #inside my computer
CLIENT = pymongo.MongoClient('mongodb_pipe')
DB = CLIENT.twitter_data #declare a db



def authenticate():
    """
    Function used for handling twitter authentification
    """
    auth = OAuthHandler(cfg['CONSUMER_API_KEY'],cfg['CONSUMER_API_SECRET'])
    auth.set_access_token(cfg['ACCESS_TOKEN'],cfg['ACCESS_TOKEN_SECRET'])
    return auth


def write_tweet(tweet_dict):
    df = pd.DataFrame(index=[0,1],data=tweet_dict)
    df.to_csv('test.csv',mode='a')

def load_into_mongo(t):
    """
    twitter_data is the DB, tweets2 is the collection, tweet_dict is the document
    """
    DB.tweets2.insert(t)


# We use an already existing class
class TwitterStreamer(StreamListener):

    def on_data(self, data):
        """
        Whatever we put in this method defines what is done with every single
        tweet as it is intercepted in real time
        """
        tweet = json.loads(data)

        if tweet['retweeted'] == False and 'RT' not in tweet['text'] and tweet['in_reply_to_status_id'] == None:
            if 'extended_tweet' in tweet:
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']

            string = text
            new_string = ''
            for i in string.split():
                s, n, p, pa, q, f = urllib.parse.urlparse(i)
                if s and n:
                    pass
                elif i[:1] == '@':
                    pass
                elif i[:1] == '#':
                    new_string = new_string.strip() + ' ' + i[1:]
                else:
                    new_string = new_string.strip() + ' ' + i

            tweet_dict = {'user':tweet['user']['screen_name'],
                        'date_stamp':datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'timestamp': datetime.datetime.timestamp(datetime.datetime.now()),
                        'clean_text': new_string,
                        'original_tweet':tweet}

            load_into_mongo(tweet_dict)



    def on_error(self,status):
        """ If rate-limiting occurs"""
        if status == 420:
            print(status)
            return False


if __name__=='__main__':
    """
    The following code runs ONLY if I type
    'python twitter_streamer.py' in the terminal
    """
    #1. Authenticate ourselves
    auth = authenticate()

    #2. Instantiate our Twitter StreamListener
    streamer = TwitterStreamer()

    #3. Wrap the 2 varibales into a Stream object to actually start
    # the streamer
    stream = Stream(auth,streamer)

    stream.filter(track=['impeachment'], languages=['en'])
