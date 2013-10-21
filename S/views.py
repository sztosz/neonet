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
#from qa.views import AbstractView
from qa import models
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect


class AbstractView():
    def __init__(self, request, action=None, template=None, output='html'):
        self.request = request
        self.output = output
        if template:
            self.template = __package__ + '/' + template + '/' + self.__class__.__name__.lower() \
                + '.' + self.output
        else:
            self.template = __package__ + '/' + self.__class__.__name__.lower() \
                + '.' + self.output
        self.output = output

        print(self.template)

        try:
            if not action:
                self.action = request.POST['action'].lower()
            else:
                self.action = action
        except MultiValueDictKeyError:
            self.action = 'view'
        self.context = dict()
        self.context['errors'] = list()
        self.context['messages'] = list()

    def _view(self):
        pass

    def _html(self):
        try:
            action = getattr(self, '_' + self.action)
            action()
        except AttributeError:
            self._view()
        return render(self.request, self.template, self.context)

    def show(self):
        try:
            output = getattr(self, '_' + self.output)
            return output()
        except AttributeError:
            return self._html()


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
        self.context['ean_form'] = forms.EanForm()


@login_required
def damage_report(request):
    page = DamageReport(request)
    return page.show()
