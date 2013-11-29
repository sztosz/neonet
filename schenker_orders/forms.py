#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-28
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django import forms
from schenker.orders import models


class Order(forms.ModelForm):
    # acronym = forms.CharField(max_length=10)

    class Meta:
        models = models.Order
        fields = ('box', 'collect_address', 'delivery_address', 'pack_amount', 'kg', 'volume', 'comment')
