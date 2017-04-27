from rest_framework import serializers

from .models import PerHourTweet, MaxRetweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerHourTweet
        fields = (
            'tweet_hour',
            'tweet_cnt'
        )


class MaxRetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaxRetweet
        fields = (
            'tweet_day',
            'tweet_retweet_cnt',
            'tweet_id',
            'tweet_text'
        )


# tweet_day = models.DateField()
# tweet_retweet_cnt = models.IntegerField()
# tweet_id = models.CharField(max_length=200, unique=True)
# tweet_text = models.TextField()