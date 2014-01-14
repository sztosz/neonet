#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.conf.urls import patterns, url
from qa import views

urlpatterns = patterns('',
                       url(r'^$', views.DamageReportsCharts.as_view(), name='index'),
                       # url(r'^damage_report_charts/&', 'qa.views.damage_report_charts', name='damage_report_charts'),
                       url(r'^damage_report_charts/$', views.DamageReportsCharts.as_view(), name='damage_report_charts'),
                       url(r'^commodity_import/$', 'qa.views.commodity_import', name='commodity_import'),
                       url(r'^damage_reports/$', views.DamageReportsFilterView.as_view(), name='damage_reports_view'),
                       url(r'^damage_reports/export/$', views.DamageReportsExport.as_view(), name='damage_report_export'),
                       url(r'^quick_commodity_list/$', views.QuickCommodityListView.as_view(),
                           name='quick_commodity_list'),
                       url(r'^quick_commodity_list/(?P<pk>\d+)/$', views.QuickCommodityListDetailView.as_view(),
                           name='quick_commodity_list_detail'),
                       url(r'^quick_commodity_list/update/(?P<pk>\d+)/$', views.QuickCommodityListUpdateView.as_view(),
                           name='quick_commodity_list_update'),
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'qa/login.html'}),
                       url(r'^logout/', 'qa.views.logout_view', name='logout'),
)
