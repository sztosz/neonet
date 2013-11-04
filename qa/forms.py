#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django import forms
from qa import models


class CommodityImportForm(forms.ModelForm):
    class Meta:
        model = models.Commodity


class CommodityBatchImportForm(forms.Form):
    file = forms.FileField(label="Wybierz plik z danymi...")


class EanForm(forms.ModelForm):
    class Meta:
        model = models.Commodity
        fields = ('ean',)


class DamageReportForm(forms.ModelForm):
    class Meta:
        model = models.DamageReport
        exclude = ('user', 'commodity',)


class DamageDetectionTimeForm(forms.ModelForm):
    class Meta:
        model = models.DamageDetectionTime
