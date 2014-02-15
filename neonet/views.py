#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth import logout


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/?next={0}'.format(request.path))
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class AbstractView():
    def __init__(self, request, action=None, module=None, template=None, output='html'):
        self.request = request
        self.output = output
        self.module = module
        self.content_type = 'text/hml'
        self.filename = 'file.txt'
        if not self.module:
            module = __package__
        if template:
            self.template = module + '/' + template + '/' + self.__class__.__name__.lower() \
                + '.' + self.output
        else:
            self.template = module + '/' + self.__class__.__name__.lower() \
                + '.' + self.output
        self.output = output

        try:
            if not action:
                self.action = request.POST['action'].lower()
        except MultiValueDictKeyError:
            self.action = 'view'
        self.context = dict()
        self.context['errors'] = list()
        self.context['messages'] = list()

    def _view(self):
        pass

    def _html(self):
        return render(self.request, self.template, self.context)

    def _file(self):
        response = HttpResponse(content_type=self.content_type)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.filename)
        try:
            response.write(self.context['file_content'])
        except MultiValueDictKeyError:
            response.write('')
        return response

    def show(self):
        try:
            action = getattr(self, '_' + self.action)
            action()
        except AttributeError:
            self._view()
        try:
            output = getattr(self, '_' + self.output)
            return output()
        except AttributeError:
            return self._html()


def index(request):
    return render(request, 'neonet/index.html', None)


def logout_view(request):
    logout(request)
    return redirect('index')
