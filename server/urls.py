"""SentimentAnalyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from server.apps.post.views import SocialNetworkViewSet
from server.apps.post.views import PostViewSet
from server.apps.post.views import TopicViewSet
from server.apps.post.views import UserViewSet
from server.apps.post.views import PlatformViewSet
# from server.apps.post.views import LocationViewSet

router = routers.DefaultRouter()
router.register(r'socialnetwork', SocialNetworkViewSet)
router.register(r'post', PostViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'user', UserViewSet)
router.register(r'platform', PlatformViewSet)
# router.register(r'location', LocationViewSet)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
