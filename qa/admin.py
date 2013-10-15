#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django.contrib import admin
from qa.models import Commodity, DamageCategory, DamageDetectionTime, DamageFurtherAction, DamageKind, DamageReport


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ean', 'sku')


class DamageCategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageDetectionTimeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageFurtherActionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageKindAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class DamageReportAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'serial')


admin.site.register(Commodity, CommodityAdmin)
admin.site.register(DamageCategory, DamageCategoryAdmin)
admin.site.register(DamageDetectionTime, DamageDetectionTimeAdmin)
admin.site.register(DamageFurtherAction, DamageFurtherActionAdmin)
admin.site.register(DamageKind, DamageKindAdmin)
admin.site.register(DamageReport, DamageReportAdmin)

