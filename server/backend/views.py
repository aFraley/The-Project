import csv

from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets

from .models import Tweet, PerHourTweet, MaxRetweet
from .serializers import TweetSerializer, MaxRetweetSerializer
from .tasks import extract_tweets_task


class TweetPerHourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PerHourTweet.objects.all()
    serializer_class = TweetSerializer


class MaxRetweetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaxRetweet.objects.all()
    serializer_class = MaxRetweetSerializer


class TweetListView(ListView):
    model = PerHourTweet


def csv_view(request):
    query = Tweet.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tweets.csv"'

    writer = csv.writer(response)
    writer.writerow(['tweet_id', 'tweet_date', 'tweet_retweet_cnt', 'tweet_favorite_cnt'])
    for row in query:
        writer.writerow([row.tweet_id, row.tweet_date, row.tweet_retweet_cnt, row.tweet_favorite_cnt])

    return response


def test(request):
    extract_tweets_task.delay()
    return HttpResponse('Tweets!')