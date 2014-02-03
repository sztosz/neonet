#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-05
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from django import forms
from qa import models
from qa.tools.parsers import validate_ean13
from django.core.exceptions import ObjectDoesNotExist


class AddDamageReportForm(forms.ModelForm):
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
        ean_is_invalid = validate_ean13(data)
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


class NewQuickCommodityListForm(forms.ModelForm):
    class Meta:
        model = models.QuickCommodityList
        exclude = ('date', 'closed',)


class AddCommodityToQuickListForm(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')

    class Meta:
        model = models.CommodityInQuickList
        fields = ('ean', 'serial', 'comment')

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = validate_ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data


class CommercialReturn(forms.ModelForm):

    class Meta:
        model = models.CommercialReturn
        fields = ('carrier', 'carrier_comment')


class CommodityInCommercialReturn(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')
    commodity = forms.CharField(widget=forms.HiddenInput(), required=False)
    commercial_return = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(CommodityInCommercialReturn, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['ean', 'commercial_return', 'commodity', 'document', 'waybill', 'unknown_origin',
                                'amount']

    class Meta:
        model = models.CommodityInCommercialReturn

    def clean_ean(self):
        ean = self.cleaned_data['ean']
        ean_is_invalid = validate_ean13(ean)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return ean

    def clean_commodity(self):
        ean = self.cleaned_data.get('ean', None)
        if ean:
            print('EAN: ' + ean)
            try:
                commodity = models.Commodity.objects.get(ean=ean)
            except models.Commodity.DoesNotExist:
                commodity = models.Commodity(sku='BRAK_TOWARU_W_BAZIE', name='BRAK_TOWARU_W_BAZIE',
                                             ean=ean)
                commodity.save()
            return commodity
        raise forms.ValidationError('')  # TODO Rewrite views, so only visible fields errors are show

    def clean_commercial_return(self):
        commercial_return = self.data['commercial_return']
        if not models.CommercialReturn.objects.filter(pk=commercial_return).exists():
            raise forms.ValidationError('Brak zwrotu w bazie, stwórz zwrot przed dodawaniem towaru')
        return models.CommercialReturn.objects.get(pk=commercial_return)

