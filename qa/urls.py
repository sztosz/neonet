#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^$', 'qa.views.index', name='index'),
                       url(r'^logout/', 'qa.views.logout_view', name='logout'),
                       url(r'^commodity_import/', 'qa.views.commodity_import', name='commodity_import'),
                       url(r'^damage_report/', 'qa.views.damage_report', name='damage_report'),
                       url(r'^damage_report_export/', 'qa.views.damage_report_export', name='damage_report_export'),
                       )
