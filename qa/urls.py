#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'qa.views.index', name='index'),
                       url(r'^logout/', 'qa.views.logout_view', name='logout'),
                       url(r'^commodity_import/', 'qa.views.commodity_import', name='commodity_import'),
                       url(r'^damage_report/', 'qa.views.damage_report', name='damage_report'),
                       url(r'^damage_report_export/', 'qa.views.damage_reports', name='damage_reports'),
                       url(r'^commodity_update_by_ean/', 'qa.views.commodity_update_by_ean',
                           name='commodity_update_by_ean'),
                       url(r'^quick_commodity_list/', 'qa.views.quick_commodity_list', name='quick_commodity_list'),
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'qa/login.html'}),
                       # url(r'^logout/$', 'django.contrib.auth.views.logout'),
                       )
