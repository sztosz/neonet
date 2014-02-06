#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, url
from qa import views

urlpatterns = patterns(
    '',
    url(r'^$', views.DamageReportsCharts.as_view(),
        name='index'),
    url(r'^damage_report_charts/$', views.DamageReportsCharts.as_view(),
        name='damage_report_charts'),
    url(r'^commodity_import/$', views.CommodityImportSingle.as_view(),
        name='commodity_import'),
    url(r'^commodity_import/batch$', views.CommodityImportBatch.as_view(),
        name='commodity_import_batch'),
    url(r'^damage_reports/$', views.DamageReports.as_view(),
        name='damage_reports_view'),
    url(r'^damage_reports/export/$', views.DamageReportsExport.as_view(),
        name='damage_report_export'),
    url(r'^damage_reports/create/$', views.DamageReportsCreate.as_view(),
        name='damage_report_create'),
    url(r'^damage_reports/update/(?P<pk>\d+)$', views.DamageReportsUpdate.as_view(),
        name='damage_report_update'),
    url(r'^quick_commodity_list/$', views.QuickCommodityList.as_view(),
        name='quick_commodity_list'),
    url(r'^quick_commodity_list/(?P<pk>\d+)/$', views.QuickCommodityListDetails.as_view(),
        name='quick_commodity_list_detail'),
    url(r'^quick_commodity_list/export/(?P<pk>\d+)/$', views.QuickCommodityListDetailsExport.as_view(),
        name='quick_commodity_list_detail_export'),
    url(r'^quick_commodity_list/update/(?P<pk>\d+)/$', views.QuickCommodityListUpdate.as_view(),
        name='quick_commodity_list_update'),
    url(r'^quick_commodity_list/close/(?P<pk>\d+)/$', views.QuickCommodityListClose.as_view(),
        name='quick_commodity_list_close'),
    url(r'^quick_commodity_list/item/update/(?P<pk>\d+)/$', views.QuickCommodityListItemUpdate.as_view(),
        name='quick_commodity_list_detail_update'),
    url(r'^quick_commodity_list/item/delete/(?P<pk>\d+)/$', views.QuickCommodityListItemDelete.as_view(),
        name='quick_commodity_list_detail_delete'),
    url(r'^commercial_return/$', views.CommercialReturns.as_view(),
        name='commercial_return'),
    url(r'^commercial_return/(?P<pk>\d+)/$', views.CommercialReturnDetail.as_view(),
        name='commercial_return_detail'),
    url(r'^commercial_return/print/(?P<pk>\d+)/$', views.CommercialReturnPrint.as_view(),
        name='commercial_return_print'),
    url(r'^commercial_return/export/(?P<pk>\d+)/$', views.CommercialReturnExport.as_view(),
        name='commercial_return_export'),
    url(r'^commercial_return/update/(?P<pk>\d+)/$', views.CommercialReturnUpdate.as_view(),
        name='commercial_return_update'),
    url(r'^commercial_return/close/(?P<pk>\d+)/$', views.CommercialReturnClose.as_view(),
        name='commercial_return_close'),
    url(r'^commercial_return/item/update/(?P<pk>\d+)/$', views.CommercialReturnItemUpdate.as_view(),
        name='commercial_return_item_update'),
    url(r'^commercial_return/item/delete/(?P<pk>\d+)/$', views.CommercialReturnItemDelete.as_view(),
        name='commercial_return_item_delete'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'qa/login.html'},
        name='login'),
    url(r'^logout/', 'qa.views.logout_view',
        name='logout'),)
