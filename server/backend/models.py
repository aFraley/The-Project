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
            .annotate(day=TruncDay('tweet_date'), hour=TruncHour('tweet_date'))\
            .values('day', 'hour').annotate(tweet_cnt=Count('tweet_id')).order_by('-day').order_by('-hour')


class MaxRetweetManager(models.Manager):
    def get_queryset(self):
        """
        get_queryset replaces objects.
        :return: max_retweet per day
        """
        return super(MaxRetweetManager, self).get_queryset()\
            .annotate(day=TruncDay('tweet_date')).values('day')\
            .annotate(max_retweet=Max('tweet_retweet_cnt')).order_by('-day')


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
    day = models.DateField()
    max_retweet = models.IntegerField()


class PerHourTweet(models.Model):
    tweet_hour = models.DateTimeField()
    tweet_cnt = models.IntegerField()

