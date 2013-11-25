#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-23
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    name = models.CharField(max_length=200)
    post_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)


class PackType(models.Model):
    name = models.CharField(max_length=50)


class Asortyment(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):

    PAYER_TYPE = (("N", "nadawca"), ("O", "odbiorca"), ("Z", "zleceniodawca"))

    # FIELDS REQUIRED
    system_type = models.BooleanField()
    box = models.BooleanField()

    collect_address = models.ForeignKey(Address)
    collect_date = models.DateField()
    delivery_address = models.ForeignKey(Address)
    delivery_date = models.DateField()
    payer_type = models.CharField(max_length=1, choices=PAYER_TYPE)

    pack_type = models.ForeignKey(PackType)
    pack_amount = models.IntegerField()
    kg = models.IntegerField()
    volume = models.IntegerField()

    asortyment = models.ForeignKey(Asortyment)

    # FIELDS OPTIONAL






