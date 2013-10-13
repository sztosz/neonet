#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com
# Create your views here.

from qa import models
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from qa import forms
from qa.tools.ExcelParser import ExcelParser

class AbstractView():
    def __init__(self, request, template=None, output='html'):
        self.request = request
        self.output = output
        if template is None:
            self.template = __package__ + '/' + self.__class__.__name__.lower() \
                            + '.' + self.output
        else:
            self.template = template
        self.output = output
        try:
            self.action = request.POST['action'].lower()
        except MultiValueDictKeyError:
            self.action = 'view'
        self.context = dict()
        self.context['errors'] = list()
        self.context['messages'] = list()

    def _view(self):
        pass

    def _html(self):
        try:
            action = getattr(self, '_' + self.action)
            action()
        except AttributeError:
            self._view()
        return render(self.request, self.template, self.context)

    def show(self):
        try:
            output = getattr(self, '_' + self.output)
            return output()
        except AttributeError:
            return self.html()


class Index(AbstractView):
    pass

class CommodityImport(AbstractView):
    def _add(self):
        form = forms.CommodityImportForm(self.request.POST)
        if form.is_valid():
            commodity = form.save()
            commodity.save()
            self.context['messages'].append('Commodity "{}" added successfully to database'.format(commodity.name))
            self.context['add_single_form'] = forms.CommodityImportForm()
        else:
            self.context['add_single_form'] = form
        self.context['batch_upload_file_form'] = forms.CommodityBatchImportForm()

    def _import(self):
        form = forms.CommodityBatchImportForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            warnings, errors = ExcelParser.parse_commodity(self.request.FILES['file'])
            for warning in warnings:
                self.context['messages'].append(warning)
            for error in errors:
                self.context['errors'].append(error)
            self.context['messages'].append('Valid data from file was uploaded')
        else:
            self.context['errors'].append('File that you were trying to upload was invalid')
        self.context['add_single_form'] = forms.CommodityImportForm()
        self.context['batch_upload_file_form'] = forms.CommodityBatchImportForm()

    def _view(self):
        self.context['batch_upload_file_form'] = forms.CommodityBatchImportForm()
        self.context['add_single_form'] = forms.CommodityImportForm()

class DamageReport(AbstractView):
    def _check_ean(self):
        form = forms.EanForm(self.request.POST)
        if form.is_valid():
            commodity = models.Commodity.objects.filter(ean=self.request.POST['ean'])
            if commodity:
                self.context['messages'].append('Commodity: {}'.format(commodity[0].name))
            else:
                self.context['messages'].append('Commodity not in database')

        else:
            self.context['messages'].append('EAN {} is invalid'.format(self.request.POST['ean']))
            self.context['ean_form'] = form

    def _add_damage_report(self):
        pass

    def _view(self):
        self.context['ean_form'] = forms.EanForm()


@login_required
def index(request):
    page = Index(request)
    return page.show()

@login_required
def commodity_import(request):
    page = CommodityImport(request)
    return page.show()

@login_required
def damage_report(request):
    page = DamageReport(request)
    return page.show()

def logout_view(request):
    logout(request)
    return redirect('qa:index')
