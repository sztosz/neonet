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


class Commodity(models.Model):
    sku = models.CharField(max_length=25, verbose_name='Index towaru (SKU)')
    ean = models.CharField(max_length=13, verbose_name='EAN')
    name = models.CharField(max_length=100, verbose_name='Nazwa towaru')

    def __unicode__(self):
        if self.name == 'BRAK_TOWARU_W_BAZIE':
            return self.ean
        else:
            return self.name


class DamageDetectionTime(models.Model):
    detection_time = models.CharField(max_length=30, verbose_name='Moment wykrycia')

    def __unicode__(self):
        return self.detection_time


class DamageCategory(models.Model):
    category = models.CharField(max_length=1, verbose_name='Kategoria uszkodzenia')
    description = models.TextField(verbose_name='Opis kategorii')

    def __unicode__(self):
        return self.category


class DamageFurtherAction(models.Model):
    further_action = models.CharField(max_length=30, verbose_name='Dalsze Postępowanie')

    def __unicode__(self):
        return self.further_action


class DamageKind(models.Model):
    damage_kind = models.CharField(max_length=30, verbose_name='Rodzaj szkody towaru')

    def __unicode__(self):
        return self.damage_kind


class DamageReport(models.Model):
    date = models.DateTimeField(verbose_name='Data utworzenia raportu')
    commodity = models.ForeignKey(Commodity, verbose_name='Towar')
    serial = models.CharField(max_length=50, verbose_name='Numer seryjny')
    brand = models.CharField(max_length=30, verbose_name='Marka')
    detection_time = models.ForeignKey(DamageDetectionTime, verbose_name='Moment wykrycia')
    category = models.ForeignKey(DamageCategory, verbose_name='Klasyfikacja uszkodzenia')
    comments = models.TextField(verbose_name='Uwagi', null=True, blank=True)
    further_action = models.ForeignKey(DamageFurtherAction, verbose_name='Dalsze Postępowanie')
    damage_kind = models.ForeignKey(DamageKind, verbose_name='Rodzaj szkody towaru')
    net_value = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Wartość towaru netto')
    user = models.ForeignKey(User, verbose_name='Użytkownik')

    def commodity_ean(self):
        return self.commodity.ean

    def unique_id(self):
        return self.date.strftime('%y%m%d%H%M%S')

    def day_str(self):
        return self.date.strftime('%Y-%m-%d')

    def __unicode__(self):
        return self.commodity.name


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
    serial = models.CharField(max_length=50, verbose_name='Numer seryjny')
    comment = models.CharField(max_length=100, verbose_name='Opis towaru')

    def __unicode__(self):
        return self.serial


class CommercialReturnCarrier(models.Model):
    name = models.CharField(max_length=50, verbose_name='Przewoźnik')

    def __unicode__(self):
        return self.name


class CommercialReturn(models.Model):
    carrier = models.ForeignKey(CommercialReturnCarrier, verbose_name='Przewoźnik')
    carrier_comment = models.CharField(max_length=50, verbose_name='Komentarz do przewoźnika', blank=True)
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
