from django.db import models
from django.db.models import Max, Count
from django.db.models.functions import TruncDay, TruncHour


class CountByHourManager(models.Manager):
    def get_queryset(self):
        """
        get_queryset replaces objects
        :return: Tweet object with max tweet_retweet_cnt
        """
        return super(CountByHourManager, self).get_queryset()\
            .annotate(tweet_day=TruncDay('tweet_date'), tweet_hour=TruncHour('tweet_date'))\
            .values('tweet_day', 'tweet_hour')\
            .annotate(tweet_cnt=Count('tweet_id'))\
            .order_by('-tweet_day')\
            .order_by('-tweet_hour')


class MaxRetweetManager(models.Manager):
    def get_queryset(self):
        """
        get_queryset replaces objects.
        :return: max_retweet per day
        """
        return super(MaxRetweetManager, self).get_queryset()\
            .annotate(tweet_day=TruncDay('tweet_date')).values('tweet_day')\
            .annotate(
                tweet_retweet_cnt=Max('tweet_retweet_cnt'),
                tweet_id=Max('tweet_id'),
                tweet_text=Max('tweet_text')
            )\
            .order_by('-tweet_day')


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=200, unique=True)
    tweet_date = models.DateTimeField()
    tweet_source = models.TextField()
    tweet_favorite_cnt = models.CharField(max_length=50)
    tweet_retweet_cnt = models.CharField(max_length=50)
    tweet_text = models.TextField()
    tweet_user = models.TextField(null=True)

    objects = models.Manager()
    tweet_count = CountByHourManager()
    max_retweet = MaxRetweetManager()

    class Meta:
        ordering = ('-tweet_date',)


class MaxRetweet(models.Model):
    tweet_day = models.DateField()
    tweet_retweet_cnt = models.IntegerField()
    tweet_id = models.CharField(max_length=200, unique=True)
    tweet_text = models.TextField()


class PerHourTweet(models.Model):
    tweet_hour = models.DateTimeField()
    tweet_cnt = models.IntegerField()

