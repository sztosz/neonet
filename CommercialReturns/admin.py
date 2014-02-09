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
from models import CommercialReturn, CommercialReturnCarrier, CommodityInCommercialReturn


class CommercialReturnCarrierAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)


class CommercialReturnAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'carrier', 'carrier_comment', 'completed',)


class CommodityInCommercialReturnAdmin(admin.ModelAdmin):
    list_display = ('commercial_return', 'commodity', 'amount', 'waybill', 'document',)

admin.site.register(CommercialReturnCarrier, CommercialReturnCarrierAdmin)
admin.site.register(CommercialReturn, CommercialReturnAdmin)
admin.site.register(CommodityInCommercialReturn, CommodityInCommercialReturnAdmin)
