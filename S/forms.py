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
from django.core.exceptions import ObjectDoesNotExist

from DamageReports import models as dr_models
from QuickCommodityLists import models as qc_models
from CommercialReturns import models as cr_models
from tools import tools


class AddDamageReportForm(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')
    serial = forms.CharField(max_length=50, label='Numer seryjny')
    brand = forms.CharField(max_length=30, label='Marka')
    category = forms.CharField(max_length=1, label='Klasyfikacja uszkodzenia')
    further_action = forms.CharField(max_length=30, label='Dalsze Postępowanie')

    class Meta:
        model = dr_models.DamageReport
        fields = ('ean', 'serial', 'brand', 'category', 'further_action', 'comments')

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = tools.validate_ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data

    def clean_category(self):
        data = self.cleaned_data['category']
        try:
            category = dr_models.DamageCategory.objects.filter(category=data)[:1].get()
            return category
        except ObjectDoesNotExist:
            raise forms.ValidationError('Wpisano niepoprawną kategorię')

    def clean_further_action(self):
        data = self.cleaned_data['further_action']
        try:
            category = dr_models.DamageFurtherAction.objects.filter(further_action=data)[:1].get()
            return category
        except ObjectDoesNotExist:
            raise forms.ValidationError('Wpisano niepoprawne dalsze postępowanie')


class DamageDetectionTimeForm(forms.ModelForm):
    class Meta:
        model = dr_models.DamageDetectionTime

    def clean_detection_time(self):
        data = self.cleaned_data['detection_time']
        try:
            detection_time = dr_models.DamageDetectionTime.objects.filter(detection_time=data)[:1].get()
            return detection_time
        except ObjectDoesNotExist:
            raise forms.ValidationError('Niepoprawny moment wykrycia')


class CheckSNForm(forms.Form):
    serial = forms.CharField(max_length=50, label='Numer seryjny')


class NewQuickCommodityListForm(forms.ModelForm):
    class Meta:
        model = qc_models.QuickCommodityList
        exclude = ('date', 'closed',)


class AddCommodityToQuickListForm(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')

    class Meta:
        model = qc_models.CommodityInQuickList
        fields = ('ean', 'serial', 'comment')

    def clean_ean(self):
        data = self.cleaned_data['ean']
        ean_is_invalid = tools.validate_ean13(data)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return data


class CommercialReturn(forms.ModelForm):

    class Meta:
        model = cr_models.CommercialReturn
        fields = ('carrier', 'carrier_comment', 'driver_name', 'car_plates')


class CommodityInCommercialReturn(forms.ModelForm):
    ean = forms.CharField(max_length=13, label='EAN')
    commodity = forms.CharField(widget=forms.HiddenInput(), required=False)
    commercial_return = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(CommodityInCommercialReturn, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['waybill', 'document', 'unknown_origin',
                                'ean', 'amount', 'commercial_return', 'commodity',
                                ]

    class Meta:
        model = cr_models.CommodityInCommercialReturn

    def clean_ean(self):
        ean = self.cleaned_data['ean']
        ean_is_invalid = tools.validate_ean13(ean)
        if ean_is_invalid:
            raise forms.ValidationError(ean_is_invalid)
        return ean

    def clean_commodity(self):
        ean = self.cleaned_data.get('ean', None)
        if ean:
            try:
                commodity = cr_models.Commodity.objects.get(ean=ean)
            except cr_models.Commodity.DoesNotExist:
                commodity = cr_models.Commodity(sku='BRAK_TOWARU_W_BAZIE', name='BRAK_TOWARU_W_BAZIE', ean=ean)
                commodity.save()
            return commodity
        raise forms.ValidationError('')  # TODO Rewrite views, so only visible fields errors are show

    def clean_commercial_return(self):
        commercial_return = self.data['commercial_return']
        if not cr_models.CommercialReturn.objects.filter(pk=commercial_return).exists():
            raise forms.ValidationError('Brak zwrotu w bazie, stwórz zwrot przed dodawaniem towaru')
        return cr_models.CommercialReturn.objects.get(pk=commercial_return)

