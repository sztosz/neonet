#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.shortcuts import render


def index(request):
    return render(request, 'neonet/index.html', None)
