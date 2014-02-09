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
    url(r'^$', DamageReportsCharts.as_view(),
        name='index'),
    url(r'^damage_report_charts/$', DamageReportsCharts.as_view(),
        name='damage_report_charts'),
    url(r'^damage_reports/$', DamageReports.as_view(),
        name='damage_reports_view'),
    url(r'^damage_reports/export/$', DamageReportsExport.as_view(),
        name='damage_report_export'),
    url(r'^damage_reports/create/$', DamageReportsCreate.as_view(),
        name='damage_report_create'),
    url(r'^damage_reports/update/(?P<pk>\d+)$', DamageReportsUpdate.as_view(),
        name='damage_report_update'),
)
