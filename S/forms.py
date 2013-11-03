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
