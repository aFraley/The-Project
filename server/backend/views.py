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
    """Return query results as a csv file."""
    query = PerHourTweet.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tweets.csv"'

    writer = csv.writer(response)
    for row in query:
        writer.writerow([row.tweet_hour, row.tweet_cnt])
    return response


def test(request):
    """
    For testing purposes;
    after a while,
    the shell becomes tedious.
    """
    extract_tweets_task.delay()
    return HttpResponse('Tweets!')
