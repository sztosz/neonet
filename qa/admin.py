#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.contrib import admin
from qa.models import Commodity

class CommodityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ean', 'sku')

admin.site.register(Commodity, CommodityAdmin)
