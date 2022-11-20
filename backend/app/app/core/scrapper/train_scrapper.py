import tweepy
import pandas as pd
import json

from app.core.config import settings

consumer_key = settings.consumer_key
consumer_secret = settings.consumer_secret
access_token = settings.access_token
access_token_secret = settings.access_token_secret

auth = tweepy.OAuth1UserHandler(
  consumer_key,
  consumer_secret,
  access_token,
  access_token_secret
)

api = tweepy.API(auth)


def search_by_words(words_file):

    dataset = pd.read_excel(words_file, index_col=None, header=None)
    #keywords = dataset.iloc[:,0] #zablokuje Twittera, do użycia przy płatnym API
    keywords = ["finanse", "zysk", "kryptowaluty", "zarób", "kasa", "zarobki", "szybki hajs", "miliony", "bogactwo", "bogacz"]
    media_types = ["images", "videos"]

    all_data = []
    for media in media_types:
        for keyword in keywords:

            tweets = api.search_tweets(keyword+" filter:"+media, tweet_mode="extended", result_type="recent", lang="pl", count=10)

            for tweet in tweets:

                if tweet.entities.get("media") is not None:
                    media_url = [one_media.get("media_url") for one_media in tweet.entities.get("media")]
                else:
                    media_url = None

                all_data.append({
                    "id": tweet.id,
                    "author_name": tweet.user.name,
                    "author_at": tweet.user.screen_name,
                    "text": tweet.full_text,
                    "hashtags": tweet.entities.get("hashtags"),
                    "mediafiles": tweet.entities.get("urls"),
                    "user_metadata": {
                        "country": tweet.user.location,
                        "age": tweet.user.created_at,
                        "total_tweets": tweet.user.statuses_count,
                        "followers": tweet.user.followers_count,
                    },
                    "media_url": media_url
                })
    return all_data


def search_by_names(names_file):

    dataset = pd.read_excel(names_file, index_col=None, header=None)
    #keywords = dataset.iloc[:, 1] #zablokuje Twittera, do użycia przy płatnym API
    keywords = ["PKOBP","BankPekaoSA","SantanderBankPL","ING__Polska", "CreditSuisse", "nbppl","mBankpl"]
    media_types = ["images", "videos"]

    all_data = []
    for media in media_types:
        for element in keywords:
            tweets = api.search_tweets(element+" filter:"+media, tweet_mode="extended", result_type="recent", lang="pl", count=10)

            for tweet in tweets:

                if tweet.entities.get("media") is not None:
                    media_url = [one_media.get("media_url") for one_media in tweet.entities.get("media")]
                else:
                    media_url = None

                all_data.append({
                "id": tweet.id,
                "author_name": tweet.user.name,
                "author_at": tweet.user.screen_name,
                "text": tweet.full_text,
                "hashtags": tweet.entities.get("hashtags"),
                "mediafiles": tweet.entities.get("urls"),
                "user_metadata": {
                    "country": tweet.user.location,
                    "age": tweet.user.created_at,
                    "total_tweets": tweet.user.statuses_count,
                    "followers": tweet.user.followers_count,
                },
                "media_url": media_url
            })
    return all_data





