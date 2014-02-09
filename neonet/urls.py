#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'neonet.views.home', name='home'),
    # url(r'^neonet/', include('neonet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'neonet.views.index', name='index'),
    url(r'^S/', include('S.urls', namespace='S')),
    url(r'^tools/', include('tools.urls', namespace='tools')),
    url(r'^returns/', include('CommercialReturns.urls', namespace='returns')),
    url(r'^commodities/', include('Commodities.urls', namespace='commodities')),
    url(r'^reports/', include('DamageReports.urls', namespace='reports')),
    url(r'^lists/', include('QuickCommodityLists.urls', namespace='lists')),

    url(r'^login/$', 'django.contrib.auth.login', {'template_name': 'qa/../templates/neonet/login.html'},
        name='login'),
    url(r'^logout/', 'neonet.views.logout_view',
        name='logout'),
)

