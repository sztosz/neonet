#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django import forms
from qa import models
from qa.tools.DataVerifier import validate_ean13


class CommodityImportForm(forms.ModelForm):
    class Meta:
        model = models.Commodity


class CommodityBatchImportForm(forms.Form):
    file = forms.FileField(label="Wybierz plik z danymi...")


class EanForm(forms.ModelForm):
    class Meta:
        model = models.Commodity
        fields = ('ean',)


class AddDamageReportForm(forms.ModelForm):
    ean = forms.CharField(max_length=13)
    commodity = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.DamageReport
        exclude = ('user',)

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = validate_ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data

    def clean_commodity(self):
        ean = self.data['ean']
        if not models.Commodity.objects.filter(ean=ean).exists():
            raise forms.ValidationError('Brak towaru w bazie')
        return models.Commodity.objects.get(ean=ean)


class CommodityUpdateByEanForm(forms.ModelForm):
    class Meta:
        model = models.Commodity
        exclude = ('sku',)

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = validate_ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data


class DamageReportsDateFilter(forms.Form):
    date_from = forms.SplitDateTimeField()
    date_to = forms.SplitDateTimeField()
