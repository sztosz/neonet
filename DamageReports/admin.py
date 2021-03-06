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

from DamageReports.models import *


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
    exclude = ('commodity', )


admin.site.register(DamageCategory, DamageCategoryAdmin)
admin.site.register(DamageDetectionTime, DamageDetectionTimeAdmin)
admin.site.register(DamageFurtherAction, DamageFurtherActionAdmin)
admin.site.register(DamageKind, DamageKindAdmin)
admin.site.register(DamageReport, DamageReportAdmin)
