#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neonet.views.home', name='home'),
    # url(r'^neonet/', include('neonet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'neonet.views.index', name='index'),
    url(r'^qa/', include('qa.urls', namespace='qa')),
    url(r'^S/', include('S.urls', namespace='S')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

