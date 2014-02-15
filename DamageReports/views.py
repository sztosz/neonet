#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals
import unicodecsv

from datetime import datetime, timedelta
from pytz import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import UpdateView, FormView, TemplateView, CreateView

from neonet.views import LoggedInMixin
from DamageReports import models
from DamageReports import forms


class DamageReports(LoggedInMixin, FormView):

    template_name = 'DamageReports/list.html'
    form_class = forms.DamageReportsDateFilter
    now = datetime.now(timezone('Europe/Warsaw'))
    yesterday = now - timedelta(days=1)
    initial = {'date_from': yesterday, 'date_to': now}

    def form_valid(self, form):
        reports = models.DamageReport.objects.select_related('commodity').filter(date__range=(
            form.cleaned_data['date_from'], form.cleaned_data['date_to']))
        return self.render_to_response(self.get_context_data(form=form, reports=reports))


class DamageReportsCreate(LoggedInMixin, CreateView):

    model = models.DamageReport
    template_name = 'DamageReports/create.html'
    form_class = forms.DamageReportForm
    now = datetime.now(timezone('Europe/Warsaw'))
    initial = {'date': now}

    def get_success_url(self):
        return reverse('DamageReports:damage_reports_view')

    def form_valid(self, form):
        report = form.save(commit=False)
        report.user = self.request.user
        report.save()
        return super(DamageReportsCreate, self).form_valid(form)


class DamageReportsUpdate(LoggedInMixin, UpdateView):

    model = models.DamageReport
    template_name = 'DamageReports/update.html'
    form_class = forms.DamageReportForm

    def get_success_url(self):
        return reverse('DamageReports:list')

    def get_initial(self):
        initial = self.initial.copy()
        initial['ean'] = self.get_object().commodity.ean
        return initial


class DamageReportsExport(LoggedInMixin, FormView):

    template_name = 'DamageReports/export.html'
    form_class = forms.DamageReportsDateFilter
    now = datetime.now(timezone('Europe/Warsaw'))
    yesterday = now - timedelta(days=1)
    initial = {'date_from': yesterday, 'date_to': now}

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')
        response['content-disposition'] = 'attachment; filename="reports.csv.txt"'
        data = models.DamageReport.objects.\
            select_related('commodity', 'detection_time', 'category', 'further_action', 'user').\
            filter(date__range=(form.cleaned_data['date_from'], form.cleaned_data['date_to']))
        writer = unicodecsv.writer(response, delimiter=b';')
        if not data:
            writer.writerow('Nie znaleziono żadnych raportów')
        else:
            for report in data:
                row = ['', unicode(report.date), report.brand, report.commodity.__unicode__(), report.serial,
                       report.detection_time.detection_time, report.category.category, report.comments,
                       report.further_action.further_action, '', '',
                       (report.user.first_name + ' ' + report.user.last_name)
                       ]
                row = [element.strip() for element in row]
                writer.writerow(row)
        return response


class DamageReportsCharts(LoggedInMixin, TemplateView):

    template_name = 'DamageReports/charts.html'

    def get_context_data(self, **kwargs):
        context = super(DamageReportsCharts, self).get_context_data(**kwargs)
        context['chart'] = self._view()
        return context

    def _view(self):

        self.a = {}
        self.b = {}
        self.c = {}

        objects = models.DamageReport.objects.select_related('category').order_by('-date')

        for report in objects:
            _date = report.day_str()

            if _date not in self.a:
                self.a[_date] = 0
            if _date not in self.b:
                self.b[_date] = 0
            if _date not in self.c:
                self.c[_date] = 0
            getattr(self, report.category.category.lower())[_date] += 1

        reports = [{'data': [], 'name': 'A'},
                   {'data': [], 'name': 'B'},
                   {'data': [], 'name': 'C'}]

        for k, v in self.a.iteritems():
            reports[0]['data'].append([k, v])
        for k, v in self.b.iteritems():
            reports[1]['data'].append([k, v])
        for k, v in self.c.iteritems():
            reports[2]['data'].append([k, v])

        return reports


