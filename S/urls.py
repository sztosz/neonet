#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r'^$', 'S.views.index', name='index'),
                       url(r'^DR/', 'S.views.damage_report', name='damage_report'),
                       url(r'^CS/', 'S.views.check_sn', name='check_sn'),
                       url(r'^QCL/', 'S.views.quick_commodity_list', name='quick_commodity_list'),
                       )
