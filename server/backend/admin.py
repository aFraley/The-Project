from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Tweet, PerHourTweet, MaxRetweet


class TweetModelAdmin(ModelAdmin):
    list_display = (
        'tweet_date',
        'tweet_id',
        'tweet_retweet_cnt',
        'tweet_favorite_cnt'
    )


class PerHourTweetModelAdmin(ModelAdmin):
    list_display = (
        'tweet_hour',
        'tweet_cnt'
    )


class MaxRetweetModelAdmin(ModelAdmin):
    list_display = (
        'tweet_day',
        'tweet_retweet_cnt',
        'tweet_id',
        'tweet_text'
    )


admin.site.register(Tweet, TweetModelAdmin)
admin.site.register(PerHourTweet, PerHourTweetModelAdmin)
admin.site.register(MaxRetweet, MaxRetweetModelAdmin)
