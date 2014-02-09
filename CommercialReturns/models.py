#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from Commodities.models import Commodity


class CommercialReturnCarrier(models.Model):
    name = models.CharField(max_length=50, verbose_name='Przewoźnik')

    def __unicode__(self):
        return self.name


class CommercialReturn(models.Model):
    carrier = models.ForeignKey(CommercialReturnCarrier, verbose_name='Przewoźnik')
    carrier_comment = models.CharField(max_length=50, verbose_name='Komentarz do przewoźnika', blank=True)
    driver_name = models.CharField(max_length=50, verbose_name='Nazwisko kierowcy', blank=True)
    car_plates = models.CharField(max_length=10, verbose_name='Nr rejestracyjny', blank=True)
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Czas Rozpoczęcia')
    end_date = models.DateTimeField(auto_now=True, verbose_name='Czas zakończenia')
    completed = models.BooleanField(verbose_name='Zakończona')
    user = models.ForeignKey(User, verbose_name='Użytkownik')

    def __unicode__(self):
        return str(self.id)

    def return_number(self):
        return 'DKJ {}'.format(str(self.id).zfill(8))


class CommodityInCommercialReturn(models.Model):
    commercial_return = models.ForeignKey(CommercialReturn, verbose_name='Zwrot handlowy')
    commodity = models.ForeignKey(Commodity, verbose_name='Towar')
    amount = models.IntegerField(verbose_name='Ilość')
    waybill = models.CharField(max_length=30, verbose_name='Numer listu przewozowego', blank=True)
    document = models.CharField(max_length=30, verbose_name='Dokument', blank=True)
    unknown_origin = models.BooleanField(verbose_name='Schenker Bezdokumentowy')

    def __unicode__(self):
        return str(self.id)

    def document_name(self):
        return 'Bezdokumentowy' if self.unknown_origin else self.document
