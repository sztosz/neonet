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
    url(r'^quick_commodity_list/$', QuickCommodityList.as_view(),
        name='quick_commodity_list'),
    url(r'^quick_commodity_list/(?P<pk>\d+)/$', QuickCommodityListDetails.as_view(),
        name='quick_commodity_list_detail'),
    url(r'^quick_commodity_list/export/(?P<pk>\d+)/$', QuickCommodityListDetailsExport.as_view(),
        name='quick_commodity_list_detail_export'),
    url(r'^quick_commodity_list/update/(?P<pk>\d+)/$', QuickCommodityListUpdate.as_view(),
        name='quick_commodity_list_update'),
    url(r'^quick_commodity_list/close/(?P<pk>\d+)/$', QuickCommodityListClose.as_view(),
        name='quick_commodity_list_close'),
    url(r'^quick_commodity_list/item/update/(?P<pk>\d+)/$', QuickCommodityListItemUpdate.as_view(),
        name='quick_commodity_list_detail_update'),
    url(r'^quick_commodity_list/item/delete/(?P<pk>\d+)/$', QuickCommodityListItemDelete.as_view(),
        name='quick_commodity_list_detail_delete'),
)
