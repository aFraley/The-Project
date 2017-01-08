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
            'day',
            'max_retweet'
        )
