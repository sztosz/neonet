#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-05
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect
from qa.tools import parsers


def sgv_ean_barcode(request, ean=None):

    if parsers.validate_ean13(ean):
        return redirect('/static/img/ean_error.svg')
    else:
        import barcode
        response = HttpResponse(content_type='image/svg+xml')
        options = {'module_height': 5, 'write_text': False}
        svg = barcode.get_barcode_class('ean13')(ean)
        response.write(svg.render(options))
        return response


