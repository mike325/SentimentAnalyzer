#!/usr/bin/env python

import logging
import argparse
import os
import sys
# import tweepy
# import json
# from yweather import Client
# from time import sleep

from django.apps import AppConfig

# from django.core.exceptions import ImproperlyConfigured

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

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.insert(0, os.path.abspath(os.path.join(_LOCALTION, '../..')))
    sys.path.insert(0, os.path.abspath(os.path.join(_LOCALTION, '../../..')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    import django
    django.setup()

from server.logger import logger
from server.apps.crawler import social

log = logger.get_logger(stream_level=_level, name=_logger_name, path=_LOCALTION)


class CrawlerConfig(AppConfig):
    name = 'crawler'


class Crawler(object):
    """ Social media crawler """

    def __init__(self, **kwards):
        super(Crawler, self).__init__()
        if 'network' not in kwards:
            raise Exception('No social network specified')

        if type(kwards['network']) == list:
            networks = kwards['network']
        elif type(kwards['network']) == str:
            networks = [kwards['network']]
        else:
            raise Exception('Network value must be either a list or a string')

        del kwards['network']

        self.networks = []
        for network in networks:
            social_class = social.get(network)
            self.networks += [social_class(**kwards)]

    def search(self, query: str, language='es', count=100):
        """TODO: Docstring for search.

        :query: TODO
        :language: TODO
        :count: TODO
        :returns: TODO

        """
        results = {}
        for network in self.networks:
            results[network.name] = network.search(query, language, count)

        return results

    def crawl(self, querys=[], repeats=1, count=100, language='es', **kwards):
        """
        """
        errors = 0
        for network in self.networks:
            try:
                network.crawl(querys=querys, repeats=repeats, count=count, language=language, **kwards)
            except NotImplementedError:
                log.error(f'Network {network.name} does not implement crawl method')
                errors += 1
        return errors


def _parseArgs():
    """ Parse CLI arguments
    :returns: argparse.ArgumentParser class instance

    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--version',
                        dest='show_version',
                        action='store_true',
                        help='print script version and exit')

    parser.add_argument('-l',
                        '--logging',
                        dest='logging',
                        default="INFO",
                        type=str,
                        help='Enable debug messages')

    parser.add_argument('-r',
                        '--repeats',
                        dest='repeats',
                        default=1,
                        type=int,
                        help='How many times should the search be repeated')

    parser.add_argument('-q',
                        '--query',
                        dest='query',
                        type=str,
                        default=None,
                        help='Search query')

    parser.add_argument('--language',
                        dest='language',
                        type=str,
                        default='es',
                        help='Change the default language of the tweets')

    parser.add_argument('--pull',
                        dest='pull',
                        type=int,
                        default=100,
                        help='Change the default number of tweets to pull')

    parser.add_argument('-t',
                        '--trend',
                        dest='trend',
                        type=str,
                        default=None,
                        help='Activate trends')

    parser.add_argument('-n',
                        '--network',
                        dest='network',
                        type=str,
                        default='twitter',
                        help='Social network where the data will be fetched')

    return parser.parse_args()


def main():
    """ Main function
    :returns: TODO

    """
    global log
    args = _parseArgs()

    if args.show_version:
        print(_version)
        return 0

    if args.logging:
        try:
            level = int(args.logging)
        except Exception:
            if args.logging.lower() == "debug":
                level = logging.DEBUG
            elif args.logging.lower() == "info":
                level = logging.INFO
            elif args.logging.lower() == "warn" or args.logging.lower() == "warning":
                level = logging.WARN
            elif args.logging.lower() == "error":
                level = logging.ERROR
            elif args.logging.lower() == "critical":
                level = logging.CRITICAL
            else:
                level = 0

    try:
        log = logger.get_logger(stream_level=level, name=_logger_name, path=_LOCALTION)
    except NameError:
        log = logging.getLogger(_logger_name,)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(logging.Formatter('[%(levelname)s] - %(message)s'))
        log.addHandler(ch)

    if (args.query is None or len(args.query) == 0) and (args.trend is None or len(args.trend) == 0):
        raise Exception('Empty querys/trends are not allow')

    log.debug(f'Version: {_version}')
    log.debug(f'Logging level: {level}')

    repeats = args.repeats
    querys = None if args.query is None else args.query.split(',')
    places = None if args.trend is None else args.trend.split(',')
    language = 'es' if args.language is None else args.language
    pull = 100 if args.pull is None else args.pull
    network = args.network.split(',')

    crawler = Crawler(network=network)

    return crawler.crawl(querys=querys, places=places, repeats=repeats, count=pull, language=language)


if __name__ == "__main__":
    main()
