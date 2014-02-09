#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from django import forms

import models
from tools import tools


class CommercialReturnItem(forms.ModelForm):
    ean = forms.CharField(max_length=13)
    commodity = forms.CharField(widget=forms.HiddenInput(), required=False)
    commercial_return = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = models.CommodityInCommercialReturn
        exclude = ('commercial_return',)

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = tools.validate_ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data

    def clean_commodity(self):
        ean = self.data['ean']
        if not models.Commodity.objects.filter(ean=ean).exists():
            raise forms.ValidationError('Brak towaru w bazie')
        return models.Commodity.objects.get(ean=ean)
