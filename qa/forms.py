#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django import forms
from qa import models


class CommodityImportForm(forms.ModelForm):
    class Meta:
        model = models.Commodity
