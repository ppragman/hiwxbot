# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 00:02:18 2015

fireTweet
This fires tweets out to the universe on my Weather Watcher Bot

@author: patrickpragman
"""

import tweepy

def fireTweet(text):
    consumerKey = 'XXXXXXX'
    consumerSecretKey = 'XXXXXXX'
    accessKey = 'XXXXXXX'
    accessSecret = 'XXXXXXX'

    auth = tweepy.OAuthHandler(consumerKey, consumerSecretKey)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)
    api.update_status(status = text)
