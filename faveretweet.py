#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
#from config import create_api
import json
import os

logger = logging.getLogger()

def create_api():
    consumer_key = os.getenv("consumer_key_MH_Pj1")
    consumer_secret = os.getenv("consumer_secret_MH_Pj1")
    access_token = os.getenv("access_token_MH_Pj1")
    access_token_secret = os.getenv("access_token_secret_MH_Pj1")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["#mentalhealth","#mentalillness","#MentalHealth","#MentalHealthAwareness","#MentalHealthMatters","#mentalhealthawareness","#mentalhealthmatters", "#SuicidePrevention"])
