from datetime import datetime, timedelta, date
import json
from pytz import timezone
import tweepy

from django.db import IntegrityError
from django.db.models import Max, Min
from django.db.models.functions import TruncDay, TruncHour

from .models import Tweet, PerHourTweet, MaxRetweet


class MaxRetweetService:
    __max_retweet = []

    def get_max_retweet(self):
        return self.__max_retweet

    def set_max_retweet(self):
        self.__max_retweet = Tweet.max_retweet.all()

    def store_max_retweet(self):
        if MaxRetweet.objects.all():
            MaxRetweet.objects.all().delete()
        for tweet in self.__max_retweet:
            MaxRetweet.objects.create(
                day=tweet['day'],
                max_retweet=tweet['max_retweet']
            )


class TweetCountService:
    __tweet_cnt = []

    def get_tweet_cnt(self):
        return self.__tweet_cnt

    def set_tweet_cnt(self):
        self.__tweet_cnt = Tweet.tweet_count.all()

    def store_tweet_cnt(self):
        if PerHourTweet.objects.all():
            PerHourTweet.objects.all().delete()
        for tweet in self.__tweet_cnt:
            PerHourTweet.objects.create(
                tweet_hour=tweet['hour'],
                tweet_cnt=tweet['tweet_cnt']
            )


class TwitterAPIService:
    """
    Get some tweets from the twitter API.
    Set up tweepy authorization on every instance.
    """
    with open('/home/alan/Code/misc/django-ember/secrets.json') as f:
        keys = json.load(f)
    __CONSUMER_KEY = keys[1]['consumer_key']
    __CONSUMER_SECRET = keys[2]['consumer_secret']
    __ACCESS_TOKEN = keys[3]['access_token']
    __ACCESS_TOKEN_SECRET = keys[4]['access_token_secret']

    __auth = tweepy.OAuthHandler(consumer_key=__CONSUMER_KEY, consumer_secret=__CONSUMER_SECRET)
    __auth.set_access_token(__ACCESS_TOKEN, __ACCESS_TOKEN_SECRET)
    __api = tweepy.API(__auth)
    __week = datetime.now(tz=timezone('US/Central')) - timedelta(days=6)
    __tweets = []

    def set_tweets(self):
        """
        Extract and store the tweets.
        If database is not empty, use oldest_tweet to get older tweets.
        If oldest_tweet.date is a week old, get younger tweets.
        """
        query = Tweet.objects.all()
        if list(query):
            oldest_tweet_id = query.aggregate(Min('tweet_id'))['tweet_id__min']
            oldest_tweet = Tweet.objects.get(tweet_id=oldest_tweet_id)
            youngest_tweet_id = query.aggregate(Max('tweet_id'))['tweet_id__max']
            if oldest_tweet.tweet_date <= self.__week:
                self.__tweets = self.__api.search(
                    q='#python',
                    since_id=youngest_tweet_id,
                    count=100
                )
            else:
                self.__tweets = self.__api.search(
                    q='#python',
                    max_id=int(oldest_tweet_id) - 1,
                    count=100
                )
        else:
            self.__tweets = self.__api.search(
                q='#python',
                count=100
            )
        if self.__tweets:
            self.store_tweets()

    def store_tweets(self):
        if Tweet.objects.all():
            Tweet.objects.filter(tweet_date__lte=self.__week).delete()
            for tweet in self.__tweets:
                try:
                    new_tweet = Tweet(
                        tweet_id=tweet.id,
                        tweet_date=tweet.created_at,
                        tweet_source=tweet.source,
                        tweet_favorite_cnt=tweet.favorite_count,
                        tweet_retweet_cnt=tweet.retweet_count,
                        tweet_text=tweet.text,
                        tweet_user=tweet.user
                    )
                    new_tweet.tweet_date = new_tweet.tweet_date - timedelta(hours=6)
                    new_tweet.tweet_date = new_tweet.tweet_date.replace(tzinfo=timezone('US/Central'))
                    new_tweet.save()
                except IntegrityError:
                    pass
