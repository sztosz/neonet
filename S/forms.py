#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-05
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django import forms
from qa import models
from qa.tools.DataVerifier import DataVerifier
from django.core.exceptions import ObjectDoesNotExist


class DamageReportForm(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')
    serial = forms.CharField(max_length=50, label='Numer seryjny')
    brand = forms.CharField(max_length=30, label='Marka')
    category = forms.CharField(max_length=1, label='Klasyfikacja uszkodzenia')
    further_action = forms.CharField(max_length=30, label='Dalsze Postępowanie')

    class Meta:
        model = models.DamageReport
        fields = ('ean', 'serial', 'brand', 'category', 'further_action', 'comments')

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = DataVerifier.ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data

    def clean_category(self):
        data = self.cleaned_data['category']
        try:
            category = models.DamageCategory.objects.filter(category=data)[:1].get()
            return category
        except ObjectDoesNotExist:
            raise forms.ValidationError('Wpisano niepoprawną kategorię')

    def clean_further_action(self):
        data = self.cleaned_data['further_action']
        try:
            category = models.DamageFurtherAction.objects.filter(further_action=data)[:1].get()
            return category
        except ObjectDoesNotExist:
            raise forms.ValidationError('Wpisano niepoprawne dalsze postępowanie')


class DamageDetectionTimeForm(forms.ModelForm):
    class Meta:
        model = models.DamageDetectionTime

    def clean_detection_time(self):
        data = self.cleaned_data['detection_time']
        try:
            detection_time = models.DamageDetectionTime.objects.filter(detection_time=data)[:1].get()
            return detection_time
        except ObjectDoesNotExist:
            raise forms.ValidationError('Niepoprawny moment wykrycia')


class CheckSNForm(forms.Form):
    serial = forms.CharField(max_length=50, label='Numer seryjny')

