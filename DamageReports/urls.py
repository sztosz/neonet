#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url

from DamageReports.views import *

urlpatterns = patterns(
    '',
    url(r'^$', DamageReports.as_view(),
        name='list'),
    url(r'^charts/$', DamageReportsCharts.as_view(),
        name='charts'),
    url(r'^export/$', DamageReportsExport.as_view(),
        name='export'),
    url(r'^create/$', DamageReportsCreate.as_view(),
        name='create'),
    url(r'^update/(?P<pk>\d+)$', DamageReportsUpdate.as_view(),
        name='update'),
)
