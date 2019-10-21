#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import with_statement

from django.db import models

import random
# from typing import Dict
# import os
# import sys
# import platform

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


def analyze(data: models.Model):
    """
    Random analyzer

    :data: model.Model: Model structure with the list of query results
    :returns: Dict[str, float]: Return a dictionary with the following key,values
        :negative: int: number of negative tweets
        :positive: int: number of positive tweets
        :neuter: int: number of neuter tweets
        :result: float: the average result of the total tweets

    """
    size = data.count()
    negative = random.randint(0, size)
    positive = random.randint(0, size - negative)
    neutre = size - negative - positive
    result = random.uniform(-1, 1)
    rsp = {
        'negative': negative,
        'positive': positive,
        'neuter': neutre,
        'result': result,
    }
    return rsp
