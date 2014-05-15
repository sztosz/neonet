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

from Commodities.models import Commodity


class QuickCommodityList(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nazwa paczki towarów')
    date = models.DateTimeField(verbose_name='Data utworzenia')
    comment = models.CharField(max_length=100, verbose_name='Opis paczki')
    closed = models.BooleanField(verbose_name='Czy zamknięta')

    def __unicode__(self):
        return self.name


class CommodityInQuickList(models.Model):
    list = models.ForeignKey(QuickCommodityList, verbose_name='Lista')
    commodity = models.ForeignKey(Commodity, verbose_name='Towar')
    serial = models.CharField(max_length=50, verbose_name='Numer seryjny', null=True)
    comment = models.CharField(max_length=100, verbose_name='Opis towaru', null=True)

    def __unicode__(self):
        return self.serial
