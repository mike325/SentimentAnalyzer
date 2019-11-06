#!/usr/bin/env python

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


def list():
    """TODO: Docstring for list.
    :returns: TODO

    """
    import os
    import traceback
    import importlib

    location = os.path.dirname(os.path.abspath(__file__))
    debug = True if 'DEBUG' in os.environ else False
    modules = []

    _, dirs, __ = next(os.walk(location))

    for candidate in dirs:
        try:
            analyzer = importlib.import_module('.' + candidate + '.analyzer', __name__)
            _ = analyzer.__getattribute__('analyze')
        except Exception:
            if debug:
                traceback.print_exc()
        else:
            modules += [candidate]

    return modules


def get(module: str):
    """

    :module: TODO
    :returns: TODO

    """
    import importlib

    try:
        analyzer = importlib.import_module('.' + module + '.analyzer', __name__)
        return analyzer.__getattribute__('analyze')
    except Exception:
        raise NotImplementedError(f'The module {module} does not exists')
