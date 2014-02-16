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
from django.views.generic import ListView, DetailView, CreateView, FormView

from neonet.views import LoggedInMixin
import models


class List(LoggedInMixin, ListView):

    queryset = models.Document.objects.order_by('-start_date')
    template_name = None  # TODO add template


class Details(LoggedInMixin, DetailView):

    model = models.Document
    template_name = None  # TODO add template
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super(Details, self).get_context_data(**kwargs)
        context['commodities'] = models.CommodityInDocument.objects.filter(document=self.object.pk)
        return context


class DocumentCreate(LoggedInMixin, FormView):

    model = models.Document
    template_name = None  # TODO add template
    form_class = None  # TODO add template, remember that user is excluded

    def get_success_url(self):
        return None  # TODO add template

    def form_valid(self, form):
        # TODO rewrite in some sensible manner
        f = self.request.FILES['file']
        try:
            r = unicodecsv.reader(f, encoding='utf-8')
            csv = list(r)
            document = form.save(commit=False)
            document.user = self.request.user
            document.save()
            for row in csv:
                try:
                    amount = int(row[2].split(',')[0])
                    commodity = models.Commodity.objects.get(sku=row[1])
                    obj = models.CommodityInDocument(document=document,
                                                     commodity=commodity,
                                                     amount_on_document=amount,
                                                     amount_scanned=0)
                    obj.save()
                except ValueError as e:
                    print e
                except models.Commodity.DoesNotExist:
                    pass  # TODO correct way for handling items on documents that are not present in database
        except Exception as e:
            raise e  # TODO catch any errors, and maybe later deal with them gracefully
        return super(DocumentCreate, self).form_valid(form)

