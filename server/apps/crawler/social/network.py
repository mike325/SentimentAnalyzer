#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import with_statement

from server.logger import logger
from server.apps.post.models import Topic
from server.apps.post.models import Platform
from server.apps.post.models import SocialNetwork
from server.apps.post.models import Post
from server.apps.post.models import User

from datetime import datetime

import logging
import os

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

_LOCALTION = os.path.dirname(os.path.abspath(__file__))

DEBUG = True if 'DEBUG' in os.environ else False
_logger_name = os.path.basename(__file__).split('.')[0]
_level = logging.DEBUG if DEBUG else logging.INFO

log = logger.get_logger(stream_level=_level, name=_logger_name, path=_LOCALTION)


class Network(object):
    """ Social network super class """
    def __init__(self):
        super(Network, self).__init__()
        self.name = 'Generic'

    def get_or_create_topic(self, query: str):
        """TODO: Docstring for get_user.
        :returns: TODO

        """

        if self.topic_exists(query):
            topic = Topic.objects.get(topic=query)
        else:
            log.debug(f'Creating new Topic: {query}')
            topic = Topic(topic=query)
            topic.save()

        return topic

    def get_or_create_platform(self, name: str):
        """TODO: Docstring for get_user.
        :returns: TODO

        """

        if self.platform_exists(name):
            platform = Platform.objects.get(name=name)
        else:
            log.debug(f'Creating new Platform: {name}')
            platform = Platform(name=name)
            platform.save()

        return platform

    def get_or_create_network(self):
        """TODO: Docstring for get_user.
        :returns: TODO

        """
        if self.network_exists():
            network = SocialNetwork.objects.get(name=self.name)
        else:
            log.debug(f'Creating new social Network {self.name}')
            network = SocialNetwork(name=self.name)
            network .save()

        return network

    def get_or_create_user(self, id: str, name: str, username: str, friends: int, verified: bool, network: SocialNetwork):
        """TODO: Docstring for get_user.
        :returns: TODO

        """

        if self.user_exists(username, network):
            user = User.objects.get(user_id=id)
        else:
            log.debug(f'Creating new User: {id}')
            user = User()
            user.user_id = id
            user.name = name
            user.username = username
            user.friends = friends
            user.verified = verified
            user.network = network
            user.save()

        return user

    def get_or_create_post(self, id: str, text: str, shares: int, date: datetime, favorite: int, language: str, user: User, network: SocialNetwork, platform: Platform):
        """TODO: Docstring for get_user.
        :returns: TODO

        """
        if self.post_exists(id, text):
            log.debug(f'Creating new post: {id}')
            post = Post()
            post.post_id = id
            post.text = text
            # log.debug(f'Tweet text: {post.text}')
            post.shares = shares
            post.create_date = date
            post.favorite = favorite
            post.language = language
            post.user = user
            post.network = network
            post.platform = platform
            post.save()
        else:
            post = Post.objects.get(post_id=id)

        return post

    def user_exists(self, username: str, network: SocialNetwork):
        """TODO: Docstring for user_exists.

        :id: TODO
        :returns: TODO

        """
        return User.objects.filter(username=username, network__id=network.id).exists()

    def topic_exists(self, query: str):
        """TODO: Docstring for user_exists.

        :id: TODO
        :returns: TODO

        """
        return Topic.objects.filter(topic=query).exists()

    def network_exists(self):
        """TODO: Docstring for get_user.
        :returns: TODO

        """
        return SocialNetwork.objects.filter(name=self.name).exists()

    def platform_exists(self, name: str):
        """TODO: Docstring for get_user.
        :returns: TODO

        """

        return Platform.objects.filter(name=name).exists()

    def post_exists(self, id: str, text: str = ""):
        """TODO: Docstring for get_user.
        :returns: TODO

        """
        if text == "":
            return Post.objects.filter(post_id=id).exists()
        return Post.objects.filter(post_id=id, text=text).exists()

    def stream_search(self, query: str, language: str, **kwards):
        """TODO: Docstring for real_time.

        :query: TODO
        :language: TODO
        :kwards: TODO
        :returns: TODO

        """
        raise NotImplementedError('stream_search is not implemented in Network class')

    def search(self, query: str, language: str, count: int, **kwards):
        """TODO: Docstring for search.

        :query: TODO
        :language: TODO
        :count: TODO
        :kwards: TODO
        :returns: TODO

        """
        raise NotImplementedError('search is not implemented in Network class')

    def crawl(self, *args, **kwards):
        """TODO: Docstring for search.

        :args: TODO
        :kwards: TODO
        :returns: TODO

        """
        raise NotImplementedError('crawl is not implemented in Network class')
