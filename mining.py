import tweepy
from tweepy import OAuthHandler
import keys
import json

def process_or_store(tweet):
    print(json.dumps(tweet))
 
#Authorization process
consumer_key = keys.CONSUMER_KEY
consumer_secret = keys.CONSUMER_SECRET
access_token = keys.ACCESS_TOKEN
access_secret = keys.ACCESS_SECRET
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#Cursor is to iterate through different obejcts

#Read our own timeline
#for status in tweepy.Cursor(api.home_timeline).items(10):
    #print(status.text)

#List of my tweets
for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json)