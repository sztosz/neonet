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
    url(r'^commercial_return/$', CommercialReturns.as_view(),
        name='commercial_return'),
    url(r'^commercial_return/(?P<pk>\d+)/$', CommercialReturnDetail.as_view(),
        name='commercial_return_detail'),
    url(r'^commercial_return/print/(?P<pk>\d+)/$', CommercialReturnPrint.as_view(),
        name='commercial_return_print'),
    url(r'^commercial_return/export/(?P<pk>\d+)/$', CommercialReturnExport.as_view(),
        name='commercial_return_export'),
    url(r'^commercial_return/update/(?P<pk>\d+)/$', CommercialReturnUpdate.as_view(),
        name='commercial_return_update'),
    url(r'^commercial_return/close/(?P<pk>\d+)/$', CommercialReturnClose.as_view(),
        name='commercial_return_close'),
    url(r'^commercial_return/item/update/(?P<pk>\d+)/$', CommercialReturnItemUpdate.as_view(),
        name='commercial_return_item_update'),
    url(r'^commercial_return/item/delete/(?P<pk>\d+)/$', CommercialReturnItemDelete.as_view(),
        name='commercial_return_item_delete'),
)

