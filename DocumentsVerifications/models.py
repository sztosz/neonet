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


class Document(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nazwa dokuemetu')
    date_entered = models.DateTimeField(auto_now_add=True, verbose_name='Czas Rozpoczęcia')
    end_date = models.DateTimeField(auto_now=True, verbose_name='Czas zakończenia')
    completed = models.BooleanField(verbose_name='Sprawdzony')
    user = models.ForeignKey(User, verbose_name='Użytkownik')


class CommodityInDocument(models.Model):
    document = models.ForeignKey(Document, verbose_name='Nazwa dokuemetu')
    commodity = models.ForeignKey(Commodity, verbose_name='Towar')
    amount_on_document = models.IntegerField(verbose_name='Ilość na dokumencie')
    amount_scanned = models.IntegerField(verbose_name='Ilość zeskanowanych')
