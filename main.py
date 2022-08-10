import csv
import json
import os
import random
import time

import tweepy
from dotenv import load_dotenv

load_dotenv()

jsonLang = []
with open('lang.csv') as csvf:
    csvReader = csv.DictReader(csvf)

    for row in csvReader:
        jsonLang.append(row)

smolLang = {}
for x in jsonLang:
    smolLang[x["HUMAN"]] = x["SMOL"]


def translate(sentence):
    return " ".join([smolLang.get(x, x) for x in sentence.split()])


translate("i had the idea to buy eth")
exit(0)
auth = tweepy.OAuth1UserHandler(consumer_key=os.environ.get("API_KEY"),
                                consumer_secret=os.environ.get("API_SECRET"),
                                access_token=os.environ.get("ACCESS_TOKEN"),
                                access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"))

apiV1 = tweepy.API(auth)

api = tweepy.Client(consumer_key=os.environ.get("API_KEY"),
                    consumer_secret=os.environ.get("API_SECRET"),
                    access_token=os.environ.get("ACCESS_TOKEN"),
                    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"))


class SmolListener(tweepy.StreamingClient):
    def __init__(self):
        super().__init__(bearer_token=os.environ.get("BEARER"))

    def on_data(self, raw_data):
        print(f'Received: {raw_data}')
        replyID = json.loads(raw_data.decode("utf-8"))['data']['id']
        try:
            referencedTweet = \
                api.get_tweet(id=replyID, user_auth=True, expansions=["referenced_tweets.id"])[1]['tweets'][0]
            apiV1.lookup_friendships()
            api.create_tweet(text=f'💚 smol lang here 👇🏻\n\n{referencedTweet}\n\n#wassieverse',
                             in_reply_to_tweet_id=replyID)
        except Exception as err:
            print(f'Something went wrong: {err}')


stream = SmolListener()

stream.add_rules(tweepy.StreamRule("@smolhelp"))
stream.filter()
