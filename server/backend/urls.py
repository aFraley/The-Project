from rest_framework import routers

from django.conf.urls import url, include


from .views import MaxRetweetViewSet, TweetPerHourViewSet, TweetListView, csv_view


router = routers.DefaultRouter()
router.register(r'tweet-per-hour', TweetPerHourViewSet)
router.register(r'max-retweet', MaxRetweetViewSet)

urlpatterns = [
    url(r'^csv/$', csv_view),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]