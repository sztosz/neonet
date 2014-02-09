#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from django.views.generic import FormView, CreateView

from neonet.views import LoggedInMixin
import forms
from tools import tools


class CommodityImportSingle(LoggedInMixin, CreateView):

    template_name = 'Commodities/../templates/Commodities/CommodityImport_single.html'
    form_class = forms.CommodityImportSingleForm

    def get_success_url(self):
        return reverse('DamageReports:damage_reports_view')


class CommodityImportBatch(LoggedInMixin, FormView):

    template_name = 'qa/../templates/Commodities/CommodityImport_batch.html'
    form_class = forms.CommodityImportBatchForm

    def form_valid(self, form):
        tools.parse_commodity(self.request.FILES['file'])
        return super(CommodityImportBatch, self).form_valid(form)

    def get_success_url(self):
        return reverse('DamageReports:damage_reports_view')
