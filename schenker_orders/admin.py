#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-28
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django.contrib import admin
from schenker_orders.models import *


class AddressAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'street', 'post_code', 'city', )


class PackTypeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class AsortymentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'collect_address', 'delivery_address')


class OrderListAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )


admin.site.register(Address, AddressAdmin)
admin.site.register(PackType, PackTypeAdmin)
admin.site.register(Asortyment, AsortymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderList, OrderListAdmin)
