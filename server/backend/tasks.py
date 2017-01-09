from celery import shared_task

from .services import TwitterAPIService, TweetCountService, MaxRetweetService


@shared_task(name='extract_tweets_task')
def extract_tweets_task():
    """Extract tweets and count tweets per hour by day."""
    extract_tweets = TwitterAPIService()
    extract_tweets.set_tweets()

    tweet_count = TweetCountService()
    tweet_count.set_tweet_cnts()
    tweet_count.store_tweet_cnts()

    max_retweet = MaxRetweetService()
    max_retweet.set_max_retweets()
    max_retweet.store_max_retweets()
