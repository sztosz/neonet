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
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, ListView, DeleteView, RedirectView

from neonet.views import LoggedInMixin
import models
import forms


class CommercialReturns(LoggedInMixin, ListView):

    queryset = models.CommercialReturn.objects.order_by('-start_date')
    template_name = 'CommercialReturns/list.html'


class CommercialReturnDetail(LoggedInMixin, DetailView):

    model = models.CommercialReturn
    template_name = 'CommercialReturns/detail.html'
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
            writer.writerow(['Numer: {}'.format(context['commercial_return'].return_number())])
            writer.writerow(['Przewoźnik: {}'.format(context['commercial_return'].carrier.name)])
            writer.writerow(['Nazwisko kierowcy: {}'.format(context['commercial_return'].driver_name)])
            writer.writerow(['Nr rejestracyjny samochodu: {}'.format(context['commercial_return'].car_plates)])
            writer.writerow(['Komentarz do przewoźnika: {}'.format(context['commercial_return'].carrier_comment)])
            writer.writerow(['Czas trwania: {} - {}'.format(context['commercial_return'].start_date,
                                                            context['commercial_return'].end_date)])
            writer.writerow(['Kontroler: {} {}'.format(context['commercial_return'].user.first_name,
                                                       context['commercial_return'].user.last_name)])
            writer.writerow([''])
            writer.writerow(['Ilość', 'Towar', 'ean', 'List przewozowy', 'Dokument'])
            for row in context['commodities']:
                writer.writerow([row.amount, row.commodity, row.commodity.ean, row.waybill, row.document_name()])
        except KeyError:
            writer.writerow(['Nastąpił błąd parsowania danych: brak towarów w liście'])
        return response


class CommercialReturnPrint(CommercialReturnDetail):

    template_name = 'CommercialReturns/print.html'


class CommercialReturnUpdate(LoggedInMixin, UpdateView):

    model = models.CommercialReturn
    template_name = 'CommercialReturns/update.html'

    def get_success_url(self):
        return reverse('DamageReports:list')


class CommercialReturnClose(LoggedInMixin, RedirectView):

    url = reverse_lazy('DamageReports:list')

    def get_redirect_url(self, *args, **kwargs):
        commercial_return = models.CommercialReturn.objects.get(pk=self.kwargs.get('pk'))
        commercial_return.completed = True
        commercial_return.save()
        return super(CommercialReturnClose, self).get_redirect_url()


class CommercialReturnItemUpdate(LoggedInMixin, UpdateView):

    model = models.CommodityInCommercialReturn
    template_name = 'CommercialReturns/item_update.html'
    form_class = forms.CommercialReturnItem

    def get_success_url(self):
        return reverse('DamageReports:commercial_return_detail', args=(self.object.commercial_return.pk,))

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
    template_name = 'CommercialReturns/item_delete.html'

    def get_success_url(self):
        return reverse('DamageReports:detail', args=(self.object.commercial_return.pk,))


def logout_view(request):
    logout(request)
    return redirect('DamageReports:charts')
