#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url

from Commodities.views import *

urlpatterns = patterns(
    '',
    url(r'^import/single/$', CommodityImportSingle.as_view(),
        name='import_single'),
    url(r'^import/batch/$', CommodityImportBatch.as_view(),
        name='import_batch'),
)
