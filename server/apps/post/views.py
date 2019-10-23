#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from django.shortcuts import render
# from django.contrib.auth.models import User, Group

import rest_framework.request
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import SocialNetwork
from .models import Location
from .models import Platform
from .models import Topic
from .models import User
from .models import Post

from .serializers import SocialNetworkSerializer
from .serializers import LocationSerializer
from .serializers import PlatformSerializer
from .serializers import TopicSerializer
from .serializers import UserSerializer
from .serializers import PostSerializer

import server.nlp as nlp
import server.settings as DEBUG

from datetime import datetime
import traceback


__header__ = """
                              -`
              ...            .o+`
           .+++s+   .h`.    `ooo/
          `+++%++  .h+++   `+oooo:
          +++o+++ .hhs++. `+oooooo:
          +s%%so%.hohhoo'  'oooooo+:
          `+ooohs+h+sh++`/:  ++oooo+:
           hh+o+hoso+h+`/++++.+++++++:
            `+h+++h.+ `/++++++++++++++:
                     `/+++ooooooooooooo/`
                    ./ooosssso++osssssso+`
                   .oossssso-````/osssss::`
                  -osssssso.      :ssss``to.
                 :osssssss/  Mike  osssl   +
                /ossssssss/   8a   +sssslb
              `/ossssso+/:-        -:/+ossss'.-
             `+sso+:-`                 `.-/+oso:
            `++:.                           `-/+/
            .`                                 `/
"""

_version = '1.0.0'
_author = 'Mike'
_mail = 'mickiller.25@gmail.com'


def get_post_by_topic(topic: int, start=None, end=None, now=None):
    """TODO: Docstring for get_user.

    :user: TODO
    :returns: TODO

    """
    if start is not None and end is not None:
        posts = Post.objects.filter(create_date__gte=start, create_date__lte=end, topics__id=topic)
    elif start is not None:
        posts = Post.objects.filter(create_date__gte=start, topics__id=topic)
    elif end is not None:
        posts = Post.objects.filter(create_date__lte=end, topics__id=topic)
    else:
        raise NotImplementedError('Now flag is not implemented')

    return posts


def get_post_by_user(user: str, start=None, end=None, now=None):
    """TODO: Docstring for get_user.

    :user: TODO
    :returns: TODO

    """
    if start is not None and end is not None:
        posts = Post.objects.filter(create_date__gte=start, create_date__lte=end, user__user_id=user)
    elif start is not None:
        posts = Post.objects.filter(create_date__gte=start, user__user_id=user)
    elif end is not None:
        posts = Post.objects.filter(create_date__lte=end, user__user_id=user)
    else:
        raise NotImplementedError('Now flag is not implemented')

    return posts


def analyze_data(filter: str, method, id, start=None, end=None, now=None):
    """TODO: Docstring for analyze_data.

    :topic: TODO
    :method: TODO
    :start: TODO
    :end: TODO
    :now: TODO
    :returns: TODO

    """

    if filter == 'topic':
        try:
            posts = get_post_by_topic(id, start, end, now)
        except NotImplementedError:
            return Response({'message': 'Now flag not implemente'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    try:
        analyze = nlp.get(method)
    except NotImplementedError:
        return Response({'message': f'The method {method} does not exists'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        if DEBUG:
            traceback.print_exc()
        return Response({'message': 'An error ocurrered, try again'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    results = analyze(posts)
    return Response(results, status=status.HTTP_200_OK)


class SocialNetworkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @action(detail=True, methods=['post'], name='Analyze sentiments of topics')
    def analyze(self, request: rest_framework.request.Request, pk=None):
        """TODO: Docstring for .

        :request: TODO
        :pk: TODO
        :returns: TODO
        """

        try:
            # data = JSONParser().parse(request.data)
            data = request.data
        except Exception:
            if DEBUG:
                traceback.print_exc()
            return Response({'message': 'Malformed json data'}, status=status.HTTP_400_BAD_REQUEST)

        if 'method' not in data:
            return Response({'message': 'Method argument is necessary'}, status=status.HTTP_400_BAD_REQUEST)

        if 'date' not in data and 'now' not in data:
            return Response({'message': 'You must either specify a date frame or give the now flag'}, status=status.HTTP_400_BAD_REQUEST)

        start = None
        end = None
        if 'date' in data:
            start = None if 'start' not in data['date'] else datetime.strptime(data['date']['start'], '%Y/%m/%d')
            end = None if 'end' not in data['date'] else datetime.strptime(data['date']['end'], '%Y/%m/%d')
        now = None if 'now' not in data else data['now']
        method = None if 'method' not in data else data['method']

        if now is not None and end is not None:
            return Response({'message': 'Now flag and end date are conflict flags'}, status=status.HTTP_400_BAD_REQUEST)

        return analyze_data('topic', method, pk, start, end, now)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], name='Get User by date')
    def analyze(self, request: rest_framework.request.Request, pk=None):
        """TODO: Docstring for .

        :request: TODO
        :pk: TODO
        :returns: TODO

        """
        pass


class PlatformViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    @action(detail=True, methods=['post'], name='Get Platform by date')
    def analyze(self, request: rest_framework.request.Request, pk=None):
        """TODO: Docstring for .

        :request: TODO
        :pk: TODO
        :returns: TODO

        """
        pass


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
