#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com
# Create your views here.

from __future__ import unicode_literals

from datetime import datetime, timedelta
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

from django.views.generic import DetailView, UpdateView, ListView, FormView, TemplateView, CreateView


MODULE = __package__


class CommodityImport(AbstractView):
    def _add(self):
        form = forms.CommodityImportSingleForm(self.request.POST)
        if form.is_valid():
            commodity = form.save()
            commodity.save()
            self.context['messages'].append('Towar "{}" został dodany poprawnie do bazy danych'.format(commodity.name))
            self.context['add_single_form'] = forms.CommodityImportSingleForm()
        else:
            self.context['add_single_form'] = form
        self.context['batch_upload_file_form'] = forms.CommodityImportBatchForm()

    def _import(self):
        form = forms.CommodityImportBatchForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            warnings, errors = ExcelParser.parse_commodity(self.request.FILES['file'])
            for warning in warnings:
                self.context['messages'].append(warning)
            for error in errors:
                self.context['errors'].append(error)
            self.context['messages'].append('Dane bez błędów zostały dodane do bazy danych')
        else:
            self.context['errors'].append('Próba importu nie powiodła się, plik jest nieproprawny')
        self.context['add_single_form'] = forms.CommodityImportSingleForm()
        self.context['batch_upload_file_form'] = forms.CommodityImportBatchForm()

    def _view(self):
        self.context['batch_upload_file_form'] = forms.CommodityImportBatchForm()
        self.context['add_single_form'] = forms.CommodityImportSingleForm()


class CommodityImportSingle(CreateView):

    template_name = 'qa/CommodityImport_single.html'
    form_class = forms.CommodityImportSingleForm

    def get_success_url(self):
        return reverse('qa:damage_reports_view')


class CommodityImportBatch(FormView):

    template_name = 'qa/CommodityImport_batch.html'
    form_class = forms.CommodityImportBatchForm

    def form_valid(self, form):
        warnings, errorrs = ExcelParser.parse_commodity(self.request.FILES['file'])
        return super(CommodityImportBatch, self).form_valid(form)

    def get_success_url(self):
        return reverse('qa:damage_reports_view')


class DamageReports(FormView):

    template_name = 'qa/DamageReports_view.html'
    form_class = forms.DamageReportsDateFilter
    now = datetime.now(timezone('Europe/Warsaw'))
    yesterday = now - timedelta(days=1)
    initial = {'date_from': yesterday, 'date_to': now}

    def form_valid(self, form):
        reports = models.DamageReport.objects.select_related('commodity').filter(date__range=(
            form.cleaned_data['date_from'], form.cleaned_data['date_to']))
        return self.render_to_response(self.get_context_data(form=form, reports=reports))


class DamageReportsCreate(CreateView):

    model = models.DamageReport
    template_name = 'qa/DamageReports_create.html'
    form_class = forms.AddDamageReportForm
    now = datetime.now(timezone('Europe/Warsaw'))
    initial = {'date': now}

    def get_success_url(self):
        return reverse('qa:damage_reports_view')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(DamageReportsCreate, self).form_valid(form)


class DamageReportsUpdate(UpdateView):

    model = models.DamageReport
    template_name = 'qa/DamageReports_update.html'
    form_class = forms.AddDamageReportForm

    def get_success_url(self):
        return reverse('qa:damage_reports')

    def get_initial(self):
        initial = self.initial.copy()
        initial['ean'] = self.get_object().commodity.ean
        return initial


class DamageReportsExportV(FormView):

    template_name = 'qa/DamageReports_export.html'
    form_class = forms.DamageReportsDateFilter

    def form_valid(self, form):
        data = damage_reports_export_to_csv(data=models.DamageReport.objects.filter(
            date__range=(form.cleaned_data['date_from'], form.cleaned_data['date_to'])))
        response = HttpResponse(data, content_type='application/csv')
        response['content-disposition'] = 'attachment; filename="reports.csv.txt"'
        return response


class DamageReportsCharts(TemplateView):

    template_name = 'qa/DamageReports_charts.html'

    def get_context_data(self, **kwargs):
        context = super(DamageReportsCharts, self).get_context_data(**kwargs)
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


class QuickCommodityList(ListView):

    queryset = models.QuickCommodityList.objects.filter(closed=False).order_by('-date')
    template_name = 'qa/QuickCommodityList_list.html'


class QuickCommodityListDetail(DetailView):

    model = models.QuickCommodityList
    template_name = 'qa/QuickCommodityList_detail.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super(QuickCommodityListDetail, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInQuickList.objects.filter(list=self.object.pk)
        return context


class QuickCommodityListUpdate(UpdateView):

    model = models.QuickCommodityList
    template_name = 'qa/QuickCommodityList_update.html'

    def get_success_url(self):
        return reverse('qa:quick_commodity_list')


@login_required(login_url='/qa/login/')
def commodity_import(request):
    page = CommodityImport(request, module=MODULE)
    return page.show()


def logout_view(request):
    logout(request)
    return redirect('qa:index')
