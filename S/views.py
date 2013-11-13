#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-21
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from datetime import datetime
from S import forms
from neonet.views import AbstractView
from qa import models
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

MODULE = __package__


class DamageReport(AbstractView):
    def _choose_detection_time(self):
        form = forms.DamageDetectionTimeForm(self.request.POST)
        if form.is_valid():
            self.request.session['report_detection_time'] = form.cleaned_data['detection_time'].detection_time
            self.context['damage_report_form'] = forms.DamageReportForm()
        else:
            #self.context['messages'].append('Niepoprawnie wybrany moment wykrycia uszkodzenia')
            self.context['damage_detection_time_form'] = form

    def _add_damage_report(self):
        form = forms.DamageReportForm(self.request.POST)
        if form.is_valid():
            damage = form.save(commit=False)
            damage.user = self.request.user
            damage.date = datetime.now()
            try:
                commodity = models.Commodity.objects.filter(ean=form.cleaned_data['ean'])[:1].get()
                damage.commodity = commodity
            except ObjectDoesNotExist:
                commodity = models.Commodity(sku='BRAK_TOWARU_W_BAZIE', name='BRAK_TOWARU_W_BAZIE',
                                             ean=form.cleaned_data['ean'])
                commodity.save()
            damage.commodity = commodity
            detection_time = self.request.session['report_detection_time']
            try:
                damage.detection_time = models.DamageDetectionTime.objects.get(detection_time=detection_time)
            except ObjectDoesNotExist:
                raise KeyError('No DETECTION_TIME in session, please contact developer')
            damage_kind = models.DamageKind.objects.get(pk=1)
            damage.damage_kind = damage_kind
            damage.net_value = 0

            damage.save()
            self.context['messages'].append('Raport zapisany poprawnie')
            self.context['damage_report_form'] = forms.DamageReportForm()
        else:
            self.context['errors'].append('Niepoprawne dane w formularzu')
            self.context['damage_report_form'] = form

    def _view(self):
        self.context['damage_detection_time_form'] = forms.DamageDetectionTimeForm()


class CheckSN(AbstractView):
    def _check(self):
        form = forms.CheckSNForm(self.request.POST)
        if form.is_valid():
            serial = form.cleaned_data['serial']
            try:
                data = models.DamageReport.objects.filter(serial=serial)
                if not data:
                    self.context['messages'].append('Serial nie został wcześniej zarejestrowany')
                else:
                    self.context['reports'] = data
            except ObjectDoesNotExist:
                self.context['messages'].append('Serial nie został wcześniej zarejestrowany')
            self.context['check_sn_form'] = forms.CheckSNForm()
        else:
            self.context['errors'].append('Niepoprawne dane w formularzu')
            self.context['check_sn_form'] = form

    def _view(self):
        self.context['check_sn_form'] = forms.CheckSNForm()


class QuickCommodityList(AbstractView):
    def _view(self):
        pass

    def _create_new_list(self):
        pass

    def _add_commodity_to_list(self):
        pass

    def _close_list(self):
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
