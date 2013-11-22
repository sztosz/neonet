#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError


class AbstractView():
    def __init__(self, request, action=None, module=None, template=None, output='html'):
        self.request = request
        self.output = output
        self.module = module
        if not self.module:
            module = __package__
        if template:
            self.template = module + '/' + template + '/' + self.__class__.__name__.lower() \
                + '.' + self.output
        else:
            self.template = module + '/' + self.__class__.__name__.lower() \
                + '.' + self.output
        self.output = output

        print(self.template)

        try:
            if not action:
                self.action = request.POST['action'].lower()
            else:
                self.action = action
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
            return self._html()


def index(request):
    return render(request, 'neonet/index.html', None)
