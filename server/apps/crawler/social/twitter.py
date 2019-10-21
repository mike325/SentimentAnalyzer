#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import with_statement

from server.logger import logger
from .network import Network
from server.apps.post.models import Post

import logging
import tweepy
import json
import os
# import sys
# import argparse
from yweather import Client
from time import sleep

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

_sleep_time = 10

log = logger.get_logger(stream_level=_level, name=_logger_name, path=_LOCALTION)


class Twitter(Network):
    """docstring for Twitter"""
    def __init__(self, secrets=None):
        super(Twitter, self).__init__()

        if secrets is not None:
            twitter = secrets
        else:
            if 'TWITTER_TOKEN_KEY' in os.environ and 'TWITTER_TOKEN_SECRET' in os.environ:
                twitter = {
                    'token': {
                        'key': os.environ['TWITTER_TOKEN_KEY'],
                        'secret': os.environ['TWITTER_TOKEN_SECRET']
                    }
                }
            elif os.path.isfile(os.path.join(_LOCALTION, 'settings.json')):
                with open(os.path.join(_LOCALTION, 'settings.json'), 'r') as secrets:
                    twitter = json.load(secrets)['twitter']
            else:
                raise Exception("There's no secrets file")

        self.name = 'Twitter'
        auth = tweepy.OAuthHandler(twitter['token']['key'], twitter['token']['secret'])
        self.api = tweepy.API(auth)

    def stream_search(self, query: str, language: str, **kwards):
        """TODO: Docstring for real_time.

        :query: TODO
        :language: TODO
        :count: TODO
        :kwards: TODO
        :returns: TODO

        """
        raise NotImplementedError('Stream search not implemented yet')

    def search(self, query: str, language: str = 'es', count: int = 100, **kwards):
        """TODO: Docstring for search.

        :query: TODO
        :language: TODO
        :returns: TODO

        """

        if query is None or len(query) == 0:
            raise Exception('Empty querys are not allow')

        query = query.lower()
        tweets = self.api.search(query, lang=language, count=count, tweet_mode='extended')

        log.debug(f'Getting search for {query}; fetch {len(tweets)}')

        if len(tweets) == 0:
            log.debug('No results were return')
            return

        network = self.get_or_create_network()
        topic = self.get_or_create_topic(query)

        for tweet in tweets:
            try:
                text = tweet.retweeted_status.full_text
            except AttributeError:
                text = tweet.full_text

            if self.post_exists(tweet.id, text):

                platform = self.get_or_create_platform(tweet.source)
                user = self.get_or_create_user(tweet.user.id, tweet.user.name, tweet.user.screen_name, tweet.user.friends_count, network)

                log.debug(f'Adding new Topic to Post: {topic.topic}')
                post = self.get_or_create_post(tweet.id, text, tweet.retweet_count, tweet.created_at, tweet.favorite_count, language, user, network, platform)
                post.topics.add(topic)
                if 'hashtags' in tweet.entities and len(tweet.entities['hashtags']) > 0:
                    for hashtag in tweet.entities['hashtags']:
                        query = f"#{hashtag['text'].lower()}"
                        topic = self.get_or_create_topic(query)
                        post.topics.add(topic)
                post.save()
            elif self.post_exists(tweet.id):
                post = Post.objects.get(post_id=tweet.id)
                post.favorite = tweet.favorite_count
                post.shares = tweet.retweet_count
                post.save()
                log.debug(f'Adding new Topic to Post: {topic.topic}')
                post.topics.add(topic)

        return tweets

    def crawl(self, querys=[], places=[], repeats=1, count=100, trend_threshold=500, language='es'):
        """TODO: Docstring for get_data.
        :returns: TODO

        """
        if repeats <= 0:
            log.error('Repeats must be an integer greater than 0')
            return -1

        if querys is list and len(querys) > 0:
            log.debug(f'Querys {",".join(querys)}')

        if places is list and len(places) > 0:
            log.debug(f'Places {",".join(places)}')

        for i in range(0, repeats):
            if querys is not None and len(querys) > 0:
                for j in range(0, len(querys)):
                    query = querys[j]
                    log.info(f'Getting search for {query}')
                    self.search(query, count=count, language=language)
                    if j < len(querys) - 1:
                        sleep(_sleep_time)

            if places is not None and len(places) > 0:
                woei_client = Client()
                for j in range(0, len(places)):
                    place = places[j]
                    place_id = woei_client.fetch_woeid(place)
                    log.debug(f'Getting trendings for {place}')
                    trendings = self.api.trends_place(place_id)
                    trendings = trendings[0]['trends']
                    for k in range(0, len(trendings)):
                        trend = trendings[k]
                        if trend['tweet_volume'] is not None and trend['tweet_volume'] > trend_threshold:
                            log.info(f'Getting Trend {trend["name"]} with {trend["tweet_volume"]} tweets')
                            self.search(trend['name'], count=count, language=language)
                            if k < len(trendings) - 1:
                                sleep(_sleep_time)
                    if j < len(places) - 1:
                        sleep(_sleep_time)
            if i < repeats - 1:
                sleep(_sleep_time)

        return 0
