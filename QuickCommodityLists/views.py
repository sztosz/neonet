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
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, ListView, DeleteView

from neonet.views import LoggedInMixin
import models
import forms


class QuickCommodityList(LoggedInMixin, ListView):

    queryset = models.QuickCommodityList.objects.filter(closed=False).order_by('-date')
    template_name = 'QuickCommodityLists/list.html'


class QuickCommodityListUpdate(LoggedInMixin, UpdateView):

    model = models.QuickCommodityList
    template_name = 'QuickCommodityLists/update.html'

    def get_success_url(self):
        return reverse('QuickCommodityLists:detail', args=(self.object.pk,))


class QuickCommodityListClose(LoggedInMixin, DetailView):

    model = models.QuickCommodityList

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.closed = True
        obj.save()
        return redirect('QuickCommodityLists:list')


class QuickCommodityListDetails(LoggedInMixin, DetailView):

    model = models.QuickCommodityList
    template_name = 'QuickCommodityLists/detail.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super(QuickCommodityListDetails, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInQuickList.objects.filter(list=self.object.pk)
        return context


class QuickCommodityListDetailsExport(QuickCommodityListDetails):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quick_list.csv.txt"'

        writer = unicodecsv.writer(response, delimiter=b';')
        try:
            writer.writerow(['Nazwa: {}'.format(context['list'].name)])
            writer.writerow(['Data: {}'.format(context['list'].date)])
            writer.writerow(['Komentarz: {}'.format(context['list'].comment)])
            writer.writerow([''])
            writer.writerow(['Towar', 'Numer seryjny', 'Komentarz'])
            for row in context['commodities']:
                writer.writerow([row.commodity, row.serial, row.comment])
        except KeyError:
            writer.writerow(['Nastąpił bład parsowania danych: brak towarów w liście'])
        return response


class QuickCommodityListItemUpdate(LoggedInMixin, UpdateView):

    model = models.CommodityInQuickList
    template_name = 'QuickCommodityLists/item_update.html'
    form_class = forms.QuickCommodityListItem

    def get_success_url(self):
        return reverse('QuickCommodityLists:detail', args=(self.object.list.pk,))

    def get_initial(self):
        initial = self.initial.copy()
        initial['ean'] = self.get_object().commodity.ean
        return initial


class QuickCommodityListItemDelete(LoggedInMixin, DeleteView):

    model = models.CommodityInQuickList
    template_name = 'QuickCommodityLists/delete.html'

    def get_success_url(self):
        return reverse('QuickCommodityLists:detail', args=(self.object.list.pk,))

