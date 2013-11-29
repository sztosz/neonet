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
    acronym = models.CharField(max_length=10)

    def __unicode__(self):
        return self.acronym


class PackType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Asortyment(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

#class Rod(models.Model):
#    rod_type = models.CharField(max_length=100)
#    rod_no = models.CharField(max_length=30)
#    rod_amount = models.IntegerField()
#    order = models.ForeignKey(Order)
#
#
#class Reference(models.Model):
#    ref_no = models.CharField(max_length=100)
#    ref_type = models.IntegerField()
#    order = models.ForeignKey(Order)


class OrderList(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Order(models.Model):

    PAYER_TYPE = (("N", "nadawca"), ("O", "odbiorca"), ("Z", "zleceniodawca"))

    order_list = models.ForeignKey(OrderList)

    # FIELDS REQUIRED
    system_type = models.BooleanField()
    box = models.BooleanField()

    collect_address = models.ForeignKey(Address, related_name='order_collect_address')
    collect_date = models.DateField()
    delivery_address = models.ForeignKey(Address, related_name='order_delivery_address')
    delivery_date = models.DateField()
    payer_type = models.CharField(max_length=1, choices=PAYER_TYPE)

    pack_type = models.ForeignKey(PackType)
    pack_amount = models.IntegerField()
    kg = models.DecimalField(decimal_places=2, max_digits=5)
    volume = models.DecimalField(decimal_places=2, max_digits=5)

    asortyment = models.ForeignKey(Asortyment)

    comment = models.TextField(max_length=160)

    # FIELDS OPTIONAL

    #client_no_collect = models.CharField(max_length=100)
    #nr_palet_collect = models.IntegerField()
    #client_no_delivery = models.CharField(max_length=100)
    #nr_palet_delivery = models.IntegerField()
    #pallet_place = models.IntegerField()
    #
    #mb = models.DecimalField()
    #
    #adr = models.BooleanField()
    #adr_un = models.CharField(max_length=4)
    #adr_name = models.CharField(max_length=250)
    #adr_gr = models.CharField(max_length=4)
    #adr_nieprzekr = models.BooleanField()
    #
    #deliv_10 = models.BooleanField()
    #deliv_sat = models.BooleanField()
    #isotherm = models.BooleanField()
    #promotion = models.BooleanField()
    #docum_tow = models.BooleanField()
    #zabezpieczenie = models.CharField(max_length=100)
    #deliv_hiper = models.BooleanField()
    #HACCP = models.BooleanField()
    #pobranie = models.IntegerField()
    #polecenie_odbioru = models.BooleanField()
    #rod_avail = models.IntegerField

    def __unicode__(self):
        return self.comment
        #return "{} FROM: {}, TO: {}".format(self.comment, self.collect_address, self.delivery_address)


