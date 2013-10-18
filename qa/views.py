#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com
# Create your views here.

from __future__ import unicode_literals

from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from qa import models
from qa import forms
from qa.tools.ExcelParser import ExcelParser
import csv

class AbstractView():
    def __init__(self, request, action=None, template=None, output='html'):
        self.request = request
        self.output = output
        if template is None:
            self.template = __package__ + '/' + self.__class__.__name__.lower() \
                            + '.' + self.output
        else:
            self.template = template
        self.output = output

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
            return self.html()


class Index(AbstractView):
    pass

class CommodityImport(AbstractView):
    def _add(self):
        form = forms.CommodityImportForm(self.request.POST)
        if form.is_valid():
            commodity = form.save()
            commodity.save()
            self.context['messages'].append('Towar "{}" został dodany poprawnie do bazy danych'.format(commodity.name))
            self.context['add_single_form'] = forms.CommodityImportForm()
        else:
            self.context['add_single_form'] = form
        self.context['batch_upload_file_form'] = forms.CommodityBatchImportForm()

    def _import(self):
        form = forms.CommodityBatchImportForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            warnings, errors = ExcelParser.parse_commodity(self.request.FILES['file'])
            for warning in warnings:
                self.context['messages'].append(warning)
            for error in errors:
                self.context['errors'].append(error)
            self.context['messages'].append('Dane bez błędów zostały dodane do bazy danych')
        else:
            self.context['errors'].append('Próba importu nie powiodła się, plik jest nieproprawny')
        self.context['add_single_form'] = forms.CommodityImportForm()
        self.context['batch_upload_file_form'] = forms.CommodityBatchImportForm()

    def _view(self):
        self.context['batch_upload_file_form'] = forms.CommodityBatchImportForm()
        self.context['add_single_form'] = forms.CommodityImportForm()

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
            self.context['ean_form'] = forms.EanForm()

    def _view(self):
        self.context['ean_form'] = forms.EanForm()

class DamageReportExport():
    def __init__(self, request):
        self.request = request

    @staticmethod
    def show():
        #response = HttpResponse(content_type='text/csv')
        #response['Content-Disposition'] = 'attachment; filename="damage_report.csv"'
        #writer = csv.writer(response)
        #damage_reports = models.DamageReport.objects.all()
        #for report in damage_reports:
        #    writer.writerow(['', report.date, report.brand, report.commodity.name, report.serial,
        #                     report.detection_time.detection_time, report.category.category, report.comments,
        #                     report.further_action.further_action, report.further_kind.damage_kind]
        #    )
        #return response
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="damage_report.txt"'
        damage_reports = models.DamageReport.objects.all()
        output = u''
        for report in damage_reports:
            output += u'"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{} {}";\r\n'.format('', report.date, report.brand,
                                    report.commodity.name, report.serial, report.detection_time.detection_time,
                                    report.category.category, report.comments, report.further_action.further_action,
                                    report.damage_kind.damage_kind, report.user.first_name, report.user.last_name)
        response.write(output)
        return response


@login_required
def index(request):
    page = Index(request)
    return page.show()

@login_required
def commodity_import(request):
    page = CommodityImport(request)
    return page.show()

@login_required
def damage_report(request):
    page = DamageReport(request)
    return page.show()

@login_required
def damage_report_export(request):
    page = DamageReportExport(request)
    return page.show()

def logout_view(request):
    logout(request)
    return redirect('qa:index')
