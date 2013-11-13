#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

# Create your models here.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Commodity(models.Model):
    sku = models.CharField(max_length=25, verbose_name='Index towaru (SKU)')
    ean = models.CharField(max_length=13, verbose_name='EAN')
    name = models.CharField(max_length=100, verbose_name='Nazwa towaru')

    def __unicode__(self):
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

    def __unicode__(self):
        return self.commodity.name


class QuickCommodityList(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nazwa paczki towarów')
    date = models.DateTimeField(verbose_name='Data utworzenia')
    comment = models.CharField(max_length=100, verbose_name='Opis paczki')

    def __unicode__(self):
        return self.name


class CommodityInList(models.Model):
    commodity = models.ForeignKey(Commodity, verbose_name='Towar')
    serial = models.CharField(max_length=50, verbose_name='Numer seryjny')
    comment = models.CharField(max_length=100, verbose_name='Opis paczki')
