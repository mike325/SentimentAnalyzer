#!/usr/bin/env python

import logging
import os
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


def get_logger(file_level=None, stream_level=None, name='dummy', path='.'):
    if stream_level is None:
        stream_level = logging.ERROR

    if file_level is None:
        file_level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(os.path.join(path, name + '.log'), mode='a')
    fh.setLevel(file_level)

    ch = logging.StreamHandler()
    ch.setLevel(stream_level)

    fh.setFormatter(logging.Formatter('[%(levelname)s] - %(message)s'))
    ch.setFormatter(logging.Formatter('[%(levelname)s] - %(message)s'))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    pass
