from django.conf.urls import url, include
from rest_framework import routers

from rest_framework.authtoken.views import obtain_auth_token
from accounts.views import UserViewSet
from backend import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tweet-per-hour', views.TweetPerHourViewSet)
router.register(r'max-retweet', views.MaxRetweetViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^api-token-auth/', obtain_auth_token),
	url(r'api/', include(router.urls))
]
