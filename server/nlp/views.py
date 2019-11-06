#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from django.shortcuts import render
# from django.contrib.auth.models import User, Group

# import rest_framework.request
# from rest_framework import viewsets
# from rest_framework.decorators import action
# # from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# from .models import SocialNetwork
# from .models import Location
# from .models import Platform
# from .models import Topic
# from .models import User
# from .models import Post

import server.nlp as nlp
# import server.settings as DEBUG

# from datetime import datetime
# import traceback


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


@api_view(['GET'])
def method_list(request):
    """TODO: Docstring for platexists.

    :request: TODO
    :returns: TODO

    """

    data = {
        'methods': nlp.list()
    }

    return Response(data, status=status.HTTP_200_OK)
