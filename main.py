import csv
import json
import os
import re

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
    linksRemoved = [re.sub(r'http\S+', '', x) for x in sentence.split()]
    return " ".join([smolLang.get(x, x) for x in linksRemoved if x != ''])


api = tweepy.Client(consumer_key=os.environ.get("API_KEY"),
                    consumer_secret=os.environ.get("API_SECRET"),
                    access_token=os.environ.get("ACCESS_TOKEN"),
                    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"))


class SmolListener(tweepy.StreamingClient):
    def __init__(self):
        super().__init__(bearer_token=os.environ.get("BEARER"))

    def on_data(self, raw_data):
        print(f'Received: {raw_data}')
        try:
            replyID = json.loads(raw_data.decode("utf-8"))['data']['id']
            referencedTweet = api.get_tweet(
                id=replyID,
                user_auth=True,
                expansions=["referenced_tweets.id", "in_reply_to_user_id"]
            )
            try:
                referencedText = referencedTweet[1]['tweets'][0].text
                taggedPerson = referencedTweet[1]['users'][0].username

                api.create_tweet(
                    text=f'“{translate(referencedText)}” - @{taggedPerson}\n\n#wassieverse',
                    in_reply_to_tweet_id=replyID
                )
            except Exception as err:
                print(f'Crashed but can reply: {err}')
                api.create_tweet(text=f'aw soz i haz crushed dunno why ~_~\n\n#wassieverse',
                                 in_reply_to_tweet_id=replyID)
        except Exception as err:
            print(f'Something went wrong: {err}')


stream = SmolListener()

stream.add_rules(tweepy.StreamRule("@smolquote"))
stream.filter()