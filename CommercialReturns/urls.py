#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns(
    '',
    url(r'^$', CommercialReturns.as_view(),
        name='list'),
    url(r'^(?P<pk>\d+)/$', CommercialReturnDetail.as_view(),
        name='detail'),
    url(r'^print/(?P<pk>\d+)/$', CommercialReturnPrint.as_view(),
        name='print'),
    url(r'^export/(?P<pk>\d+)/$', CommercialReturnExport.as_view(),
        name='export'),
    url(r'^update/(?P<pk>\d+)/$', CommercialReturnUpdate.as_view(),
        name='update'),
    url(r'^close/(?P<pk>\d+)/$', CommercialReturnClose.as_view(),
        name='close'),
    url(r'^item/update/(?P<pk>\d+)/$', CommercialReturnItemUpdate.as_view(),
        name='item_update'),
    url(r'^item/delete/(?P<pk>\d+)/$', CommercialReturnItemDelete.as_view(),
        name='item_delete'),
)

