#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django.contrib import admin
from qa.models import *


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ean', 'sku', )


class DamageCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageDetectionTimeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageFurtherActionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageKindAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageReportAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'serial', 'commodity_ean', )
    # fields = ('commodity_ean', )
    exclude = ('commodity', )


class QuickCommodityListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date', 'closed', )


class CommodityInQuickListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'list', 'commodity', 'serial', )


admin.site.register(Commodity, CommodityAdmin)
admin.site.register(DamageCategory, DamageCategoryAdmin)
admin.site.register(DamageDetectionTime, DamageDetectionTimeAdmin)
admin.site.register(DamageFurtherAction, DamageFurtherActionAdmin)
admin.site.register(DamageKind, DamageKindAdmin)
admin.site.register(DamageReport, DamageReportAdmin)
admin.site.register(QuickCommodityList, QuickCommodityListAdmin)
admin.site.register(CommodityInQuickList, CommodityInQuickListAdmin)
