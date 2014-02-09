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

from models import Commodity


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ean', 'sku', )


admin.site.register(Commodity, CommodityAdmin)
