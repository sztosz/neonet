#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

# Create your models here.

from __future__ import unicode_literals

from django.db import models


class Commodity(models.Model):
    sku = models.CharField(max_length=25, verbose_name='Product Index (SKU)')
    ean = models.CharField(max_length=13, verbose_name='EAN')
    name = models.CharField(max_length=100, verbose_name='Product Name')

    def __unicode__(self):
        return self.name

class DamageDetectionTime(models.Model):
    detection_time = models.CharField(max_length=30, verbose_name='Detection Time')

    def __unicode__(self):
        return self.detection_time

class DamageCategory(models.Model):
    category = models.CharField(max_length=1, verbose_name='Category')
    description = models.TextField(verbose_name='Category description')

    def __unicode__(self):
        return self.category

class DamageFurtherAction(models.Model):
    further_action = models.CharField(max_length=30, verbose_name='Further Action')

    def __unicode__(self):
        return self.further_action

class DamageKind(models.Model):
    damage_kind = models.CharField(max_length=30, verbose_name='Damage Kind')

    def __unicode__(self):
        return self.damage_kind

class DamageReport(models.Model):
    date = models.DateTimeField(verbose_name='Date of report entry')
    commodity = models.ForeignKey(Commodity, verbose_name='Product')
    serial = models.CharField(max_length=50, verbose_name='Serial Number')
    brand = models.CharField(max_length=30, verbose_name='Brand')
    detection_time = models.ForeignKey(DamageDetectionTime, verbose_name='Detection Time')
    category = models.ForeignKey(DamageCategory, verbose_name='Damage Category')
    comments = models.TextField(verbose_name='Comments')
    further_action = models.ForeignKey(DamageFurtherAction, verbose_name='Further Action')
    further_kind = models.ForeignKey(DamageKind, verbose_name='Damage Kind') # TODO CHANGE THE NAME!

    def __unicode__(self):
        return self.commodity.name










