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
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \n\'])|(\w+:\/\/\S+)|(www.\S+)",
            '',
            x).lower() for x in sentence.split(sep=" ")]
    return " ".join(
        [smolLang.get(x, x) for x in linksRemoved if x != '']
    ).strip().replace("imp", "inp")


api = tweepy.Client(consumer_key=os.environ.get("API_KEY"),
                    consumer_secret=os.environ.get("API_SECRET"),
                    access_token=os.environ.get("ACCESS_TOKEN"),
                    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"))


class SmolListener(tweepy.StreamingClient):
    def __init__(self):
        super().__init__(bearer_token=os.environ.get("BEARER"))

    def on_data(self, raw_data):
        print(f'NEW TWEET >>> {raw_data.decode("utf-8")}')
        try:
            jsoned = json.loads(raw_data.decode("utf-8"))
            replyID = jsoned['data']['id']
            authorName = jsoned['includes']['users'][0]['username']

            referencedTweet = api.get_tweet(
                id=replyID,
                user_auth=True,
                expansions=["referenced_tweets.id", "in_reply_to_user_id", "author_id"]
            )
            try:
                try:
                    # check if first tweet
                    refTweetText = referencedTweet.includes["tweets"][0].text
                    refTweetUsernames = [x.username for x in referencedTweet[1]["users"]]
                    currentText = referencedTweet.data.text.replace(refTweetText, "")
                    for i in refTweetUsernames:
                        currentText = currentText.replace(i, "").strip()

                    referencedText = referencedTweet[1]['tweets'][0].text

                    # tag to self post
                    if len(referencedTweet[1]['users']) == 1:
                        taggedPerson = referencedTweet[1]['users'][0].username
                    else:
                        taggedPerson = referencedTweet[1]['users'][1].username

                    if authorName == "smolquote":
                        print(f'Skip, author is bot')
                        return
                    elif taggedPerson == "smolquote":
                        print(f'Skip, person replied to bot')
                        return
                    elif "@smolquote" not in currentText:
                        print(f'Skip, smolbot was not tagged')
                        return

                except:
                    raise Exception(f'>>> Post is unkown: {raw_data.decode("utf-8")}')

                referencedTranslated = translate(referencedText)
                newTweetText = f'“{referencedTranslated}” - @{taggedPerson}\n\n#wassieverse'

                if len(newTweetText) > 280:
                    newTweetText = f'aw smoltext haz brok ~_~'
                elif referencedTranslated == "":
                    newTweetText = f'tbw i kant translate noting O_o'

                api.create_tweet(
                    text=newTweetText,
                    in_reply_to_tweet_id=replyID
                )
            except Exception as err:
                print(f'CRASH >>> {err}')

        except Exception as err:
            print(f'Something went wrong: {err}')


stream = SmolListener()

stream.add_rules(tweepy.StreamRule("(@smolquote) filter:replies -is:retweet -is:quote"))
stream.filter(expansions="author_id")

print("Smol Quote Running...")
