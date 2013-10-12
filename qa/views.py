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

class AbstractView():
    def __init__(self, request, template=None, output='html'):
        self.request = request
        if template is None:
            self.template = __package__ + '/' + self.__class__.__name__.lower() \
                            + '.html'
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

    def html(self):
        try:
            action = getattr(self, '_' + self.action)
            action()
        except AttributeError:
            self._view()
        return render(self.request, self.template, self.context)

    def output(self):
        try:
            output = getattr(self, '_' + self.output)
            return output()
        except AttributeError:
            return self.html()


class Index(AbstractView):
    pass

class CommodityImport(AbstractView):
    def _import(self):
        pass

    def _add(self):
        form = forms.CommodityImportForm(self.request.POST)
        if form.is_valid():
            commodity = form.save()
            commodity.save()
            self.context['messages'].append('Commodity "{}" added successfully to database'.format(commodity.name))
            self.context['form'] = forms.CommodityImportForm()
        else:
            self.context['form'] = form

    def _view(self):
        self.context['form'] = forms.CommodityImportForm()

@login_required
def index(request):
    page = Index(request)
    return page.html()

@login_required
def commodity_import(request):
    page = CommodityImport(request)
    return page.html()

def logout_view(request):
    logout(request)
    return redirect('qa:index')
