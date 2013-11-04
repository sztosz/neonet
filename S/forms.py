#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-21
#
# @author: sztosz@gmail.com

from qa import forms as qa_forms
from django import forms
from qa import models


class EanForm(qa_forms.EanForm):
    pass


class DamageReportForm(forms.ModelForm):
    class Meta:
        model = models.DamageReport
        fields = ('serial', 'brand', 'comment', 'net_value')
        widgets = {
            'detection_time': forms.CharField(max_length=30),
            'category':       forms.CharField(max_length=1),
            'further_action': forms.CharField(max_length=30),
            'damage_kind':    forms.CharField(max_length=30),
        }


class DamageDetectionTimeForm(forms.ModelForm):
    class Meta:
        model = models.DamageDetectionTime
