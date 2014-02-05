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
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from qa import models
from qa import forms
from qa.tools.parsers import parse_commodity, damage_reports_export_to_csv
from django.views.generic import DetailView, UpdateView, ListView, FormView,\
    TemplateView, CreateView, DeleteView, RedirectView


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/qa/login/?next={0}'.format(request.path))
        return super(LoggedInMixin, self).  dispatch(request, *args, **kwargs)


class CommodityImportSingle(LoggedInMixin, CreateView):

    template_name = 'qa/CommodityImport_single.html'
    form_class = forms.CommodityImportSingleForm

    def get_success_url(self):
        return reverse('qa:damage_reports_view')


class CommodityImportBatch(LoggedInMixin, FormView):

    template_name = 'qa/CommodityImport_batch.html'
    form_class = forms.CommodityImportBatchForm

    def form_valid(self, form):
        parse_commodity(self.request.FILES['file'])
        return super(CommodityImportBatch, self).form_valid(form)

    def get_success_url(self):
        return reverse('qa:damage_reports_view')


class DamageReports(LoggedInMixin, FormView):

    template_name = 'qa/DamageReports_view.html'
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
    template_name = 'qa/DamageReports_create.html'
    form_class = forms.DamageReportForm
    now = datetime.now(timezone('Europe/Warsaw'))
    initial = {'date': now}

    def get_success_url(self):
        return reverse('qa:damage_reports_view')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(DamageReportsCreate, self).form_valid(form)


class DamageReportsUpdate(LoggedInMixin, UpdateView):

    model = models.DamageReport
    template_name = 'qa/DamageReports_update.html'
    form_class = forms.DamageReportForm

    def get_success_url(self):
        return reverse('qa:damage_reports')

    def get_initial(self):
        initial = self.initial.copy()
        initial['ean'] = self.get_object().commodity.ean
        return initial


class DamageReportsExport(LoggedInMixin, FormView):

    template_name = 'qa/DamageReports_export.html'
    form_class = forms.DamageReportsDateFilter
    now = datetime.now(timezone('Europe/Warsaw'))
    yesterday = now - timedelta(days=1)
    initial = {'date_from': yesterday, 'date_to': now}

    def form_valid(self, form):
        query = models.DamageReport.objects.\
            select_related('commodity', 'detection_time', 'category', 'further_action', 'user').\
            filter(date__range=(form.cleaned_data['date_from'], form.cleaned_data['date_to']))
        data = damage_reports_export_to_csv(data=query)
        response = HttpResponse(data, content_type='application/csv')
        response['content-disposition'] = 'attachment; filename="reports.csv.txt"'
        return response


class DamageReportsCharts(LoggedInMixin, TemplateView):

    template_name = 'qa/DamageReports_charts.html'

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


class QuickCommodityList(LoggedInMixin, ListView):

    queryset = models.QuickCommodityList.objects.filter(closed=False).order_by('-date')
    template_name = 'qa/QuickCommodityList_list.html'


class QuickCommodityListUpdate(LoggedInMixin, UpdateView):

    model = models.QuickCommodityList
    template_name = 'qa/QuickCommodityList_update.html'

    def get_success_url(self):
        return reverse('qa:quick_commodity_list')


class QuickCommodityListClose(LoggedInMixin, DetailView):

    model = models.QuickCommodityList

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.closed = True
        obj.save()
        return redirect('qa:quick_commodity_list')


class QuickCommodityListDetails(LoggedInMixin, DetailView):

    model = models.QuickCommodityList
    template_name = 'qa/QuickCommodityList_detail.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super(QuickCommodityListDetails, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInQuickList.objects.filter(list=self.object.pk)
        return context


class QuickCommodityListItemUpdate(LoggedInMixin, UpdateView):

    model = models.CommodityInQuickList
    template_name = 'qa/QuickCommodityListItem_update.html'
    form_class = forms.QuickCommodityListItem

    def get_success_url(self):
        return reverse('qa:quick_commodity_list')

    def get_initial(self):
        initial = self.initial.copy()
        initial['ean'] = self.get_object().commodity.ean
        return initial


class QuickCommodityListItemDelete(LoggedInMixin, DeleteView):

    model = models.CommodityInQuickList
    template_name = 'qa/QuickCommodityListItem_delete.html'

    def get_success_url(self):
        return reverse('qa:quick_commodity_list_detail', args=(self.object.list.pk,))


class CommercialReturns(LoggedInMixin, ListView):

    queryset = models.CommercialReturn.objects.order_by('-start_date')
    template_name = 'qa/CommercialReturn_list.html'


class CommercialReturnDetail(LoggedInMixin, DetailView):

    model = models.CommercialReturn
    template_name = 'qa/CommercialReturn_detail.html'
    context_object_name = 'commercial_return'

    def get_context_data(self, **kwargs):
        context = super(CommercialReturnDetail, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInCommercialReturn.objects.filter(commercial_return=self.object.pk)
        return context


class CommercialReturnExport(CommercialReturnDetail):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="commercial_return.csv.txt"'

        writer = unicodecsv.writer(response, delimiter=b';')
        try:
            writer.writerow(['Numer: {}'.format(context['commercial_return'].return_number)])
            writer.writerow(['Przewoźnik: {}'.format(context['commercial_return'].carrier.name)])
            writer.writerow(['Komentarz do przewoźnika: {}'.format(context['commercial_return'].carrier_comment)])
            writer.writerow(['Czas trwania: {} - {}'.format(context['commercial_return'].start_date,
                                                            context['commercial_return'].end_date)])
            writer.writerow(['Kontroler: {} {}'.format(context['commercial_return'].user.first_name,
                                                       context['commercial_return'].user.last_name)])
            writer.writerow([''])
            writer.writerow(['Ilość', 'Towar', 'ean', 'List przewozowy', 'Dokument'])
            for row in context['commodities']:
                writer.writerow([row.amount, row.commodity, row.commodity.ean, row.waybill,
                                 'bezdokumentowy' if row.unknown_origin else row.document])
        except KeyError:
            writer.writerow(['Nastąpił bład parsowania danych: brak towarów w liście'])
        return response


class CommercialReturnPrint(CommercialReturnDetail):

    template_name = 'qa/CommercialReturn_print.html'


class CommercialReturnUpdate(LoggedInMixin, UpdateView):

    model = models.CommercialReturn
    template_name = 'qa/CommercialReturn_update.html'

    def get_success_url(self):
        return reverse('qa:commercial_returns')


class CommercialReturnClose(LoggedInMixin, RedirectView):

    url = reverse_lazy('qa:commercial_returns')

    def get_redirect_url(self, *args, **kwargs):
        commercial_return = models.CommercialReturn.objects.get(pk=self.kwargs.get('pk'))
        commercial_return.completed = True
        commercial_return.save()
        return super(CommercialReturnClose, self).get_redirect_url()


class CommercialReturnItemUpdate(LoggedInMixin, UpdateView):

    model = models.CommodityInCommercialReturn
    template_name = 'qa/CommercialReturnItem_update.html'
    form_class = forms.CommercialReturnItem

    def get_success_url(self):
        return reverse('qa:commercial_return_detail', args=(self.object.commercial_return.pk,))

    def get_initial(self):
        initial = self.initial.copy()
        initial['ean'] = self.get_object().commodity.ean
        initial['commercial_return'] = self.get_object().commercial_return.id
        return initial

    def form_valid(self, form):
        commercial_return = models.CommercialReturn.objects.get(pk=form.cleaned_data['commercial_return'])
        item = form.save(commit=False)
        item.commercial_return = commercial_return
        item.save()
        return super(CommercialReturnItemUpdate, self).form_valid(form)


class CommercialReturnItemDelete(LoggedInMixin, DeleteView):

    model = models.CommodityInCommercialReturn
    template_name = None  # TODO

    def get_success_url(self):
        return reverse('qa:commercial_return_detail', args=(self.object.list.pk,))


def logout_view(request):
    logout(request)
    return redirect('qa:index')
