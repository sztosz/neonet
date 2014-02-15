#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url

from QuickCommodityLists.views import *

urlpatterns = patterns(
    '',
    url(r'^$', QuickCommodityList.as_view(),
        name='list'),
    url(r'^(?P<pk>\d+)/$', QuickCommodityListDetails.as_view(),
        name='detail'),
    url(r'^export/(?P<pk>\d+)/$', QuickCommodityListDetailsExport.as_view(),
        name='export'),
    url(r'^update/(?P<pk>\d+)/$', QuickCommodityListUpdate.as_view(),
        name='update'),
    url(r'^close/(?P<pk>\d+)/$', QuickCommodityListClose.as_view(),
        name='close'),
    url(r'^item/update/(?P<pk>\d+)/$', QuickCommodityListItemUpdate.as_view(),
        name='item_update'),
    url(r'^item/delete/(?P<pk>\d+)/$', QuickCommodityListItemDelete.as_view(),
        name='item_delete'),
)
