#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-21
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from datetime import datetime
from pytz import timezone
from S import forms
from neonet.views import AbstractView
from qa import models
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

MODULE = __package__


class AddDamageReport(AbstractView):
    def _choose_detection_time(self):
        form = forms.DamageDetectionTimeForm(self.request.POST)
        if form.is_valid():
            self.request.session['report_detection_time'] = form.cleaned_data['detection_time'].detection_time
            self.context['damage_report_form'] = forms.AddDamageReportForm()
        else:
            self.context['damage_detection_time_form'] = form

    def _add_damage_report(self):
        form = forms.AddDamageReportForm(self.request.POST)
        if form.is_valid():
            damage = form.save(commit=False)
            damage.user = self.request.user
            damage.date = datetime.now(timezone('Europe/Warsaw'))
            print(damage.date)
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
            self.context['damage_report_form'] = forms.AddDamageReportForm()
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
    def _create_new_list(self):
        form = forms.NewQuickCommodityListForm(self.request.POST)
        if form.is_valid():
            commodity_list = form.save(commit=False)
            commodity_list.date = datetime.now(timezone('Europe/Warsaw'))
            commodity_list.closed = False
            commodity_list.save()
            self.context['new_quick_commodity_list_form'] = forms.NewQuickCommodityListForm()
        else:
            self.context['new_quick_commodity_list_form'] = form
        self.context['quick_commodity_list'] = models.QuickCommodityList.objects.filter(closed=False)

    def _add_commodity_to_list(self):
        form = forms.AddCommodityToQuickListForm(self.request.POST)
        try:
            list_id = self.request.POST['list_id'].lower()
            self.request.session['quick_commodity_list_id'] = list_id
        except MultiValueDictKeyError:
            try:
                list_id = self.request.session['quick_commodity_list_id']
            except MultiValueDictKeyError:
                self.context['messages'].append('Niepoprawnie wybrana lista, proszę zgłosić administratorowi')
                return self._view()
        if form.is_valid():
            commodity_in_list = form.save(commit=False)
            commodity_in_list.list = models.QuickCommodityList.objects.get(id=list_id)
            try:
                commodity = models.Commodity.objects.get(ean=form.cleaned_data['ean'])
            except ObjectDoesNotExist:
                commodity = models.Commodity(sku='BRAK_TOWARU_W_BAZIE', name='BRAK_TOWARU_W_BAZIE',
                                             ean=form.cleaned_data['ean'])
                commodity.save()
            commodity_in_list.commodity = commodity
            commodity_in_list.save()
            self.context['commodity_to_quick_list_form'] = forms.AddCommodityToQuickListForm()
        else:
            self.context['commodity_to_quick_list_form'] = form
        self.context['commodity_in_quick_list'] = models.CommodityInQuickList.objects.filter(list=list_id)

    def _view(self):
        self.context['quick_commodity_list'] = models.QuickCommodityList.objects.filter(closed=False)
        self.context['new_quick_commodity_list_form'] = forms.NewQuickCommodityListForm()


class Index(AbstractView):
    def _view(self):
        self.context['user'] = self.request.user.username


@login_required
def damage_report(request):
    page = AddDamageReport(request, module=MODULE)
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
