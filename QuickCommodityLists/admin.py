#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from django.contrib import admin
from models import QuickCommodityList, CommodityInQuickList


class QuickCommodityListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date', 'closed', )


class CommodityInQuickListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'list', 'commodity', 'serial', )


admin.site.register(QuickCommodityList, QuickCommodityListAdmin)
admin.site.register(CommodityInQuickList, CommodityInQuickListAdmin)

