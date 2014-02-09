#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from django import forms

import models


class CommodityImportSingleForm(forms.ModelForm):
    class Meta:
        model = models.Commodity


class CommodityImportBatchForm(forms.Form):
    file = forms.FileField(label="Wybierz plik z danymi...")

