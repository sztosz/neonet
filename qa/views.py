#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com
# Create your views here.

from __future__ import unicode_literals

from datetime import datetime, timedelta, date
from pytz import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from qa import models
from qa import forms
from qa.tools.parsers import ExcelParser, damage_reports_export_to_csv
from neonet.views import AbstractView

# from django.utils.datastructures import MultiValueDictKeyError

from django.views.generic import DetailView, UpdateView, ListView, FormView, TemplateView


MODULE = __package__


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


class AddDamageReport(AbstractView):
    def _check_ean(self):
        form = forms.EanForm(self.request.POST)
        try:
            ean = self.request.POST['ean']
        except KeyError:
            ean = 'EAN NIE ZOSTAŁ PODANY!'
        if form.is_valid():
            commodity = models.Commodity.objects.get(ean=ean)
            if commodity:
                self.context['messages'].append('TOWAR: {}'.format(commodity.name))
                self.context['messages'].append('SKU: {}'.format(commodity.sku))
                self.request.session['commodity'] = commodity.pk
                form = forms.AddDamageReportForm(initial={'date': datetime.now(timezone('Poland'))})
                self.context['damage_report_form'] = form
            else:
                self.context['messages'].append('Brak towaru w bazie z EAN\'em {}'.format(ean))
                self.context['ean_form'] = form

        else:
            self.context['messages'].append('EAN {} jest niepoprawny'.format(ean))
            self.context['ean_form'] = form

    def _add_damage_report(self):
        form = forms.AddDamageReportForm(self.request.POST)
        if form.is_valid():
            damage = form.save(commit=False)
            damage.user = self.request.user
            damage.commodity = models.Commodity.objects.get(pk=self.request.session.pop('commodity'))
            damage.save()
            self.context['messages'].append('Raport zapisany poprawnie')
        else:
            self.context['errors'].append('Niepoprawne dane w formularzu')
            self.context['damage_report_form'] = form

    def _view(self):
        self.context['ean_form'] = forms.EanForm()


class DamageReportsExport(FormView):

    template_name = 'qa/DamageReportExport_file.html'
    form_class = forms.DamageReportsExportDateFilter

    def form_valid(self, form):
        data = damage_reports_export_to_csv(data=models.DamageReport.objects.filter(
            date__range=(form.cleaned_data['date_from'], form.cleaned_data['date_to'])))
        response = HttpResponse(data, content_type='application/csv')
        response['content-disposition'] = 'attachment; filename="reports.csv.txt"'
        return response


class QuickCommodityListView(ListView):
    queryset = models.QuickCommodityList.objects.filter(closed=False).order_by('-date')


class QuickCommodityListDetailView(DetailView):
    model = models.QuickCommodityList
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super(QuickCommodityListDetailView, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInQuickList.objects.filter(list=self.object.pk)
        return context


class QuickCommodityListUpdateView(UpdateView):
    model = models.QuickCommodityList
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse('qa:quick_commodity_list')


class DamageReports(TemplateView):
    template_name = 'qa/DamageReports_chart.html'

    def get_context_data(self, **kwargs):
        context = super(DamageReports, self).get_context_data(**kwargs)
        context['chart'] = self._view()
        return context

    def _view(self):

        a, b, c = {}, {}, {}

        objects = models.DamageReport.objects.select_related('category').order_by('-date')

        for report in objects:
            _date = report.day_str()
            if report.category.category == 'A':
                if _date in a:
                    a[_date] += 1
                else:
                    a[_date] = 1
            if report.category.category == 'B':
                if _date in b:
                    b[_date] += 1
                else:
                    b[_date] = 1
            if report.category.category == 'C':
                if _date in c:
                    c[_date] += 1
                else:
                    c[_date] = 1

        reports = [{'data': [], 'name': 'A'},
                   {'data': [], 'name': 'B'},
                   {'data': [], 'name': 'C'}]

        for k, v in a.iteritems():
            reports[0]['data'].append([k, v])
        for k, v in b.iteritems():
            reports[1]['data'].append([k, v])
        for k, v in c.iteritems():
            reports[2]['data'].append([k, v])

        return reports


# class DamageReportCharts(AbstractView):
#     def _view(self):
#         reports = [{'data': [], 'name': 'A'},
#                    {'data': [], 'name': 'B'},
#                    {'data': [], 'name': 'C'}]
#         A = {}
#         B = {}
#         C = {}
#         for report in models.DamageReport.objects.order_by('-date'):
#             _date = str(date(report.date.year, report.date.month, report.date.day))
#             if report.category.category == 'A':
#                 if _date in A:
#                     A[_date] += 1
#                 else:
#                     A[_date] = 1
#             if report.category.category == 'B':
#                 if _date in B:
#                     B[_date] += 1
#                 else:
#                     B[_date] = 1
#             if report.category.category == 'C':
#                 if _date in C:
#                     C[_date] += 1
#                 else:
#                     C[_date] = 1
#         for k, v in A.items():
#             reports[0]['data'].append([k, v])
#         for k, v in B.items():
#             reports[1]['data'].append([k, v])
#         for k, v in C.items():
#             reports[2]['data'].append([k, v])
#
#         self.context['chart'] = reports


@login_required(login_url='/qa/login/')
def index(request):
    page = Index(request, module=MODULE)
    return page.show()


@login_required(login_url='/qa/login/')
def commodity_import(request):
    page = CommodityImport(request, module=MODULE)
    return page.show()


@login_required(login_url='/qa/login/')
def add_damage_report(request):
    page = AddDamageReport(request, module=MODULE)
    return page.show()

#
# @login_required(login_url='/qa/login/')
# def damage_report_export(request):
#     page = DamageReportExport(request, module=MODULE)
#     return page.show()


# @login_required(login_url='/qa/login/')
# def damage_report_charts(request):
#     page = DamageReportCharts(request, module=MODULE)
#     return page.show()


def logout_view(request):
    logout(request)
    return redirect('qa:index')
