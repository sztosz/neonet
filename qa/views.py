#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com
# Create your views here.

from __future__ import unicode_literals

from datetime import datetime, timedelta, date
# from numpy.core.tests.test_numerictypes import read_values_nested
from pytz import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from qa import models
from qa import forms
from qa.tools.ExcelParser import ExcelParser
from neonet.views import AbstractView

from django.utils.datastructures import MultiValueDictKeyError

from matplotlib import pylab
from pylab import *
import PIL
import PIL.Image
import StringIO

from collections import OrderedDict

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
                form = forms.AddDamageReportForm(initial={'date': datetime.now(timezone('Poland')),
                                                          })
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


class DamageReports(AbstractView):
    def _export(self):
        self.output = 'file'
        self.content_type = 'text/plain'
        self.filename = "damage_report.txt"
        form = forms.DamageReportViewFilter(self.request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            reports = models.DamageReport.objects.filter(date__range=(date_from, date_to))

            # reports = models.DamageReport.objects.all()
            self.context['file_content'] = u''
            for report in reports:
                self.context['file_content'] += \
                    u'"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"";"";"{} {}";\r\n'.format(
                    '', report.date, report.brand, report.commodity.__unicode__(), report.serial,
                    report.detection_time.detection_time, report.category.category, report.comments,
                    report.further_action.further_action, report.user.first_name,
                    report.user.last_name,)
        else:
            self.output = 'html'

    def _view(self):
        form = forms.DamageReportViewFilter(self.request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            reports = models.DamageReport.objects.filter(date__range=(date_from, date_to))
        else:
            now = datetime.now(timezone('Poland'))
            from_yesterday = now - timedelta(days=1)
            reports = models.DamageReport.objects.filter(date__range=(from_yesterday, now))
            form = forms.DamageReportViewFilter(initial={'date_from': from_yesterday, 'date_to': now})
        self.context['damage_reports'] = reports
        self.context['damage_reports_filter'] = form


class CommodityUpdateByEan(AbstractView):
    def _view(self):
        self.context['commodity_list'] = models.Commodity.objects.filter(name='BRAK_TOWARU_W_BAZIE')


class QuickCommodityList(AbstractView):
    def _view(self):
        self.context['quick_commodity_lists'] = models.QuickCommodityList.objects.all()

    def _list_details(self):
        try:
            list_id = self.request.POST['list_id']
        except MultiValueDictKeyError:
            self.context['messages'].append('Niepoprawnie wybrana lista, proszę zgłosić administratorowi')
            return self._view()
        self.context['quick_commodity_list'] = models.CommodityInQuickList.objects.filter(list=list_id)


class ReportsCharts(AbstractView):
    def _view(self):
        form = forms.DamageReportChartFilter()
        self.context['chart_filter_form'] = form


class Chart(AbstractView):
    def _view(self):
        self.output = 'file'
        self.filename = "chart.png"

        # Construct the graph
        # t = arange(0.0, 2.0, 0.01)
        # s = sin(2*pi*t)
        # plot(t, s, linewidth=1.0)
        #
        # xlabel('time (s)')
        # ylabel('voltage (mV)')
        # title('About as simple as it gets, folks')
        # grid(True)

        reports = models.DamageReport.objects.all()
        dates = {}
        for report in reports:
            _date = date(report.date.year, report.date.month, report.date.day)
            if _date in dates:
                dates[_date] += 1
            else:
                dates[_date] = 1
        sorted_dates = OrderedDict(sorted(dates.items(), key=lambda t: t[0]))
        # print sorted_dates
        plot(sorted_dates.keys(), sorted_dates.values(), linewidth=2.0)
        #rcParams['figure.figsize'] = 30, 3
        xlabel('Dates')
        ylabel('Number of reports')
        # ylabel.set_rotation('vertical')
        xticks( rotation=30, size='small')
        title('Number of reports per day')

        # Store image in a string buffer
        _buffer = StringIO.StringIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        pilImage.save(_buffer, "PNG")
        pylab.close()

        # Send buffer in a http response the the browser with the mime type image/png set
        self.context['file_content'] = _buffer.getvalue()
        self.content_type = 'image/png'
        # return HttpResponse(buffer.getvalue(), mimetype="image/png")




@login_required
def index(request):
    page = Index(request, module=MODULE)
    return page.show()


@login_required
def commodity_import(request):
    page = CommodityImport(request, module=MODULE)
    return page.show()


@login_required
def damage_report(request):
    page = AddDamageReport(request, module=MODULE)
    return page.show()


@login_required
def damage_reports(request):
    page = DamageReports(request, module=MODULE)
    return page.show()


@login_required
def commodity_update_by_ean(request):
    page = CommodityUpdateByEan(request, module=MODULE)
    return page.show()


@login_required
def quick_commodity_list(request):
    page = QuickCommodityList(request, module=MODULE)
    return page.show()


@login_required
def reports_charts(request):
    page = ReportsCharts(request, module=MODULE)
    return page.show()


@login_required
def chart(request):
    page = Chart(request)
    return page.show()


def logout_view(request):
    logout(request)
    return redirect('qa:index')
