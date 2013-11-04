#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-21
#
# @author: sztosz@gmail.com
# Create your views here.

from __future__ import unicode_literals

from datetime import datetime
from S import forms
from neonet.views import AbstractView
from qa import models
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect

MODULE = __package__


class DamageReport(AbstractView):
    def _check_ean(self):
        form = forms.EanForm(self.request.POST)
        try:
            ean = self.request.POST['ean']
        except KeyError:
            ean = 'EAN NIE ZOSTAŁ PODANY!'
        if form.is_valid():
            commodity = models.Commodity.objects.filter(ean=ean)
            if commodity:
                self.context['messages'].append('TOWAR: {}'.format(commodity[0].name))
                self.context['messages'].append('SKU: {}'.format(commodity[0].sku))
                print(str(commodity[0].id))
                form = forms.DamageReportForm(initial={'date':      datetime.now(),
                                                       'commodity': commodity[0],
                                                       })
                self.context['damage_report_form'] = form
            else:
                self.context['messages'].append('Brak towaru w bazie z EAN\'em {}'.format(ean))
                self.context['ean_form'] = form

        else:
            self.context['messages'].append('EAN {} jest niepoprawny'.format(ean))
            self.context['ean_form'] = form

    def _add_damage_report(self):
        form = forms.DamageReportForm(self.request.POST)
        if form.is_valid():
            damage = form.save(commit=False)
            damage.user = self.request.user
            damage.save()
            self.context['messages'].append('Raport zapisany poprawnie')
        else:
            self.context['errors'].append('Niepoprawne dane w formularzu')
            self.context['damage_report_form'] = form

    def _view(self):
        self.context['damage_detection_time_form'] = forms.DamageReportFo()


class CheckSN(AbstractView):
    pass


class QuickCommodityList(AbstractView):
    pass


class Index(AbstractView):
    def _view(self):
        self.context['user'] = self.request.user.username



@login_required
def damage_report(request):
    page = DamageReport(request, module=MODULE)
    return page.show()


@login_required
def check_sn(request):
    page = CheckSN(request, module=MODULE)
    return page.show()


@login_required
def quick_commodity_list(request):
    page = QuickCommodityList(request, module=MODULE)
    return page.show()


@login_required
def index(request):
    page = Index(request, module=MODULE)
    return page.show()
