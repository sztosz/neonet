#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-21
#
# @author: sztosz@gmail.com

from qa import forms as qa_forms
from django import forms
from qa import models


class DamageReportForm(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')
    serial = forms.CharField(max_length=50, label='Numer seryjny')
    brand = forms.CharField(max_length=30, label='Marka')
    category = forms.CharField(max_length=1, label='Klasyfikacja uszkodzenia')
    further_action = forms.CharField(max_length=30, label='Dalsze Postępowanie')

    class Meta:
        model = models.DamageReport
        fields = ('ean', 'serial', 'brand', 'category', 'further_action', 'comments')


class DamageDetectionTimeForm(forms.ModelForm):
    class Meta:
        model = models.DamageDetectionTime
