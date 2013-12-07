#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django import forms
from qa import models
from qa.tools.DataVerifier import DataVerifier


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
    class Meta:
        model = models.DamageReport
        exclude = ('user', 'commodity',)


class CommodityUpdateByEanForm(forms.ModelForm):
    class Meta:
        model = models.Commodity
        exclude = ('sku',)

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = DataVerifier.ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data

