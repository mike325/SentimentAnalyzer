#!/usr/bin/env python

import logging
import json
import os
# import sys
# import tweepy

# from typing import Dict, List
from time import sleep
from minio import Minio
from os.path import join

from server.apps.crawler.apps import Crawler
from server.logger import logger
from server.settings import DEBUG

from django.test import TestCase
from django.test import tag

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

_MINIO_SECRET_KEY = None
_MINIO_ACCESS_KEY = None
_MINIO_URL = None

_level = logging.DEBUG if DEBUG else logging.INFO
log = logger.get_logger(stream_level=_level, name=os.path.basename(__file__).split('.')[0], path=_LOCALTION)

_sleep_time = 30
Crawler._sleep_time = _sleep_time  # avoid exhausting our querys


def _setup_minio():
    """TODO: Docstring for _setup minio.
    :returns: TODO

    """
    global _MINIO_ACCESS_KEY
    global _MINIO_SECRET_KEY
    global _MINIO_URL

    if _MINIO_ACCESS_KEY is None or _MINIO_SECRET_KEY is None or _MINIO_URL is None:
        if 'MINIO_ACCESS_KEY' in os.environ or 'MINIO_SECRET_KEY' in os.environ or 'MINIO_URL' in os.environ:
            _MINIO_ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
            _MINIO_SECRET_KEY = os.environ['MINIO_SECRET_KEY']
            _MINIO_URL = os.environ['MINIO_URL']
        else:
            raise Exception("No minio key provided, can't download twitter secret file")

    minio_keys = {
        'url': _MINIO_URL,
        'access': _MINIO_ACCESS_KEY,
        'secret': _MINIO_SECRET_KEY
    }

    minioclient = Minio(minio_keys['url'],
                        access_key=minio_keys['access'],
                        secret_key=minio_keys['secret'],
                        secure=True)

    return minioclient


def _get_network_tokens(network: str):
    """TODO: Docstring for _get_network_tokens.

    :network: TODO
    :returns: TODO

    """
    settings = None
    if os.path.isfile(join(join(_LOCALTION, 'social'), 'settings.json')):
        with open(join(join(_LOCALTION, 'social'), 'settings.json'), 'r') as secrets:
            settings = json.load(secrets)
    elif network.upper() + '_TOKEN_KEY' in os.environ and network.upper() + '_TOKEN_SECRET' in os.environ:
        settings = {
            network: {
                'token': {
                    'key': '',
                    'secret': '',
                }
            }
        }
        settings[network]['token']['key'] = os.environ[network.upper() + '_TOKEN_KEY']
        settings[network]['token']['secret'] = os.environ[network.upper() + '_TOKEN_SECRET']
    else:
        minioclient = _setup_minio()
        settings = minioclient.get_object('tokens', 'settings.json')
        settings = json.loads(settings.data.decode())

    return settings


class CrawlerTest(TestCase):
    """ Test Crawler basic capabilities"""

    @tag('init')
    def test_crawler_env_init(self):
        """
        Test Crawler can be setup by environment variables
        """
        if 'TWITTER_TOKEN_KEY' not in os.environ and 'TWITTER_TOKEN_SECRET' not in os.environ:
            settings = _get_network_tokens('twitter')
            os.environ['TWITTER_TOKEN_KEY'] = settings['twitter']['token']['key']
            os.environ['TWITTER_TOKEN_SECRET'] = settings['twitter']['token']['secret']

        log.info('Testing Crawler environment init')

        self.assertIsNotNone(Crawler(network='twitter'))

    @tag('init')
    def test_crawler_file_init(self):
        """
        Test Crawler can be setup by json config file
        """
        remove = False
        settings = join(join(_LOCALTION, 'social'), 'settings.json')
        if not os.path.isfile(settings):
            minioclient = _setup_minio()
            minioclient.fget_object('twitter', 'settings.json', settings)
            remove = True

        twitter_token = {}
        if 'TWITTER_TOKEN_KEY' in os.environ:
            twitter_token['key'] = os.environ['TWITTER_TOKEN_KEY']
            del os.environ['TWITTER_TOKEN_KEY']

        if 'TWITTER_TOKEN_SECRET' in os.environ:
            twitter_token['secret'] = os.environ['TWITTER_TOKEN_SECRET']
            del os.environ['TWITTER_TOKEN_SECRET']

        try:
            log.info(f'Testing Crawler file setting init with {settings} config file')
            self.assertIsNotNone(Crawler(network='twitter'))
        finally:
            if len(twitter_token) > 0:
                if 'key' in twitter_token:
                    os.environ['TWITTER_TOKEN_KEY'] = twitter_token['key']
                if 'secret' in twitter_token:
                    os.environ['TWITTER_TOKEN_SECRET'] = twitter_token['secret']

            if remove:
                os.remove(settings)

    @tag('init')
    def test_crawler_args_init(self):
        """
        Test Crawler can be setup by passing keys as arguments
        """
        settings = _get_network_tokens('twitter')

        log.info('Testing Crawler args init')
        self.assertIsNotNone(Crawler(network='twitter', secrets=settings['twitter']))

    @tag('basic', 'core')
    def test_crawl_data(self):
        """
        Test tweets Crawler
        """
        remove = False
        if 'TWITTER_TOKEN_KEY' not in os.environ and 'TWITTER_TOKEN_SECRET' not in os.environ:
            settings = _get_network_tokens('twitter')
            os.environ['TWITTER_TOKEN_KEY'] = settings['twitter']['token']['key']
            os.environ['TWITTER_TOKEN_SECRET'] = settings['twitter']['token']['secret']
            remove = True

        log.info('Testing get_twitter_data function')

        network = 'twitter'
        tests = [
            {
                'repeats': None,
                'querys': None,
                'places': None,
            },
            {
                'repeats': 0,
                'querys': ['@Trafico_ZMG', '#jalisco'],
                'places': None,
            },
            {
                'repeats': None,
                'querys': ['Mexico', '#jalisco'],
                'places': None,
            },
            {
                'repeats': None,
                'querys': None,
                'places': ['Mexico', 'Venezuela'],
            },
            {
                'repeats': 2,
                'querys': ['@Trafico_ZMG', '#jalisco'],
                'places': ['Mexico', 'Venezuela'],
            },
        ]

        for test in tests:
            querys = [] if test['querys'] is None else test['querys']
            places = [] if test['places'] is None else test['places']
            repeats = 1 if test['repeats'] is None else test['repeats']
            if len(querys) > 0:
                log.debug('Query {}'.format(','.join(querys)))
            if len(places) > 0:
                log.debug('Places {}'.format(','.join(places)))
            log.debug('Repeats {}'.format(repeats))
            # assertion = {} if repeats > 0 else -1
            crawler = Crawler(network=network)
            # self.assertEqual(crawler.crawl(querys=querys, places=places, repeats=repeats, count=3, trend_threshold=200000), assertion)
            self.assertEqual(crawler.crawl(querys=querys, places=places, repeats=repeats, count=3, trend_threshold=200000), 0)

        if remove:
            if 'TWITTER_TOKEN_KEY' in os.environ:
                del os.environ['TWITTER_TOKEN_KEY']

            if 'TWITTER_TOKEN_SECRET' in os.environ:
                del os.environ['TWITTER_TOKEN_SECRET']

    @tag('basic', 'quick')
    def test_crawler_search(self):
        """
        Test fetching tweets as simple searches, hashtags, mentions and trending topics by country
        """
        settings = _get_network_tokens('twitter')

        log.info('Testing Basic Crawler search')
        crawler = Crawler(network='twitter', secrets=settings['twitter'])

        self.assertIsNotNone(crawler)

        tests = [
            'Mexico',
            '#jalisco',
            '@Trafico_ZMG',
        ]

        for test in tests:
            log.debug('Searching for {}'.format(test))
            # self.assertIsInstance(crawler.search(test, count=3), Dict[str, List[tweepy.models.SearchResults]])
            crawler.search(test, count=3)
            sleep(_sleep_time)
