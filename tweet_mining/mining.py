import tweepy
from tweepy import OAuthHandler
import keys
import json
import re

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

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
#for tweet in tweepy.Cursor(api.user_timeline).items():
    #process_or_store(tweet._json)

with open('mytweets.json', 'r') as f: #Save tweets into a file.json because Twitter only allows certain querys per 15 min period
    for line in f: #for every tweet in the file
        tweet = json.loads(line) #Load as python dictionary
        tokens = preprocess(tweet['text'])
        #print(json.dumps(tweet, indent=4))
        print(json.dumps(tokens, indent=3))