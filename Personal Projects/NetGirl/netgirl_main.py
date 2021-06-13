# Description: Using markivify to recreate a markov chain bot Netgirl
# Edited by: Rafael Sanchez
# June 11, 2021

import tweepy
import time
import numpy as np
import random
import datetime
import markovify

CONSUMER_KEY = "REMOVED FOR SAFETY"
CONSUMER_SECRET = "REMOVED FOR SAFETY"
ACCESS_KEY = "REMOVED FOR SAFETY"
ACCESS_SECRET = "REMOVED FOR SAFETY"

#This initializes everything
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

MIN_TIME = 60
MAX_TIME = 7200

with open("C:/Users/rafas/Documents/stuff_on_github/All Projects/Personal Projects/NetGirl/corpus.txt", encoding="utf-8") as f:
    text = f.read()

# Source: https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

while True:
    text_model = markovify.Text(text)
    msg = text_model.make_short_sentence(random.randint(100, 280))
    api.update_status(msg)
    sleep_time = random.randint(MIN_TIME, MAX_TIME)
    current_time = datetime.datetime.now()
    print("Latest Status Update: " + str(current_time) + ". Time before next tweet: " + convert(sleep_time) + ".\nNetgirl said: '" + msg + "'")
    time.sleep(sleep_time)
