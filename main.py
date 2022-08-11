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
    linksRemoved = [
        re.sub(
            "(#[A-Za-z0-9]+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \'])|(\w+:\/\/\S+)|(www.\S+)",
            '',
            x).lower() for x in sentence.split(sep=" ")]
    transformed = " ".join([smolLang.get(x, x) for x in linksRemoved if x != ''])
    return transformed.replace("imp", "inp")


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
            jsoned = json.loads(raw_data.decode("utf-8"))
            replyID = jsoned['data']['id']
            authorName = jsoned['includes']['users'][0]['username']

            if authorName == 'smolquote':
                print('Self tag, close')
                return

            referencedTweet = api.get_tweet(
                id=replyID,
                user_auth=True,
                expansions=["referenced_tweets.id", "in_reply_to_user_id", "author_id"]
            )
            try:
                referencedText = ""
                taggedPerson = ""
                try:
                    # Fetch for reply
                    referencedText = referencedTweet[1]['tweets'][0].text
                    taggedPerson = referencedTweet[1]['users'][1].username
                    if taggedPerson == "smolquote":
                        print('Reply to smolquote, close')
                        return
                    print(f'Is reply - {referencedText}')
                except:
                    try:
                        # Fetch for post
                        referencedText = referencedTweet.data.text.replace("@smolquote", "")
                        taggedPerson = referencedTweet[1]['users'][0].username
                        print(f'Is post - {referencedText}')
                    except:
                        print(f'Is not post also, raise exception')
                        raise Exception("Not post or reply")

                newTweetText = f'“{translate(referencedText)}” - @{taggedPerson}\n\n#wassieverse'

                if len(newTweetText) > 280:
                    newTweetText = f'aw smoltext bekom too long. ~_~\n\n#wassieverse'

                api.create_tweet(
                    text=newTweetText,
                    in_reply_to_tweet_id=replyID
                )
            except Exception as err:
                print(f'Crashed but can reply: {err}')
                api.create_tweet(text=f'aw soz i haz crushed dunno why ~_~\n\n#wassieverse',
                                 in_reply_to_tweet_id=replyID)
        except Exception as err:
            print(f'Something went wrong: {err}')


stream = SmolListener()

stream.add_rules(tweepy.StreamRule("(@smolquote) -filter:retweets"))
stream.filter(expansions="author_id")

print("Smol Quote Running...")
