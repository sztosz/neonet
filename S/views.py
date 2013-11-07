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
    def _choose_detection_time(self):
        form = forms.DamageDetectionTimeForm(self.request.POST)
        if form.is_valid():
            self.context['damage_report_form'] = forms.DamageReportForm(initial={'date': datetime.now()})
        else:
            self.context['messages'].append('Niepoprawnie wybrany moment wykrycia uszkodzenia')
            self.context['damage_detection_time_form'] = form

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
        self.context['damage_detection_time_form'] = forms.DamageDetectionTimeForm()


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
