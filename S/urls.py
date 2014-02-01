#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url
from S import views

urlpatterns = patterns('',
                       url(r'^$', 'S.views.index', name='index'),
                       url(r'^DR/', 'S.views.damage_report', name='damage_report'),
                       url(r'^CS/', 'S.views.check_sn', name='check_sn'),
                       url(r'^QCL/', 'S.views.quick_commodity_list', name='quick_commodity_list'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'S/login_s.html'}),
                       url(r'^CR/$', views.CommercialReturn.as_view(),
                           name='commercial_returns'),
                       url(r'^CR/create/$', views.CommercialReturnCreate.as_view(),
                           name='create_commercial_return'),
                       url(r'^CR/AddCommodity/(?P<pk>\d+)/$', views.CommercialReturnAddCommodity.as_view(),
                           name='add_commodity_to_commercial_return'),
                       url(r'^CR/Close/(?P<pk>\d+)/$', views.CommercialReturnClose.as_view(),
                           name='commercial_return_close'),
                       )
