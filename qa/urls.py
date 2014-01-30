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

urlpatterns = patterns('',
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
                       url(r'^quick_commodity_list/(?P<pk>\d+)/$', views.QuickCommodityListDetail.as_view(),
                           name='quick_commodity_list_detail'),
                       url(r'^quick_commodity_list/update/(?P<pk>\d+)/$', views.QuickCommodityListUpdate.as_view(),
                           name='quick_commodity_list_update'),
                       url(r'^quick_commodity_list/close/(?P<pk>\d+)/$', views.QuickCommodityListClose.as_view(),
                           name='quick_commodity_list_close'),
                       url(r'^quick_commodity_list_detail/update/(?P<pk>\d+)/$',
                           views.QuickCommodityListDetailUpdate.as_view(),
                           name='quick_commodity_list_detail_update'),
                       url(r'^quick_commodity_list_detail/delete/(?P<pk>\d+)/$',
                           views.QuickCommodityListDetailDelete.as_view(),
                           name='quick_commodity_list_detail_delete'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'qa/login.html'},
                           name='login'),
                       url(r'^logout/', 'qa.views.logout_view',
                           name='logout'),
                       )
