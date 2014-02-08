#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^svg_barcode/(?P<ean>\d+)/$', 'barcode_gen.views.sgv_ean_barcode', name='svg_barcode'),
)
