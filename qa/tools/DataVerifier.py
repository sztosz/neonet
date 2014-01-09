#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

EAN_WEIGHTS = '13131313131313131313131313'


def validate_ean13(ean):
    ean = str(ean)
    try:
        int(ean)
    except ValueError:
        return 'EAN może się składać tylko z cyfr'
    l = len(ean)
    if l != 13:
        return 'EAN musi posiadać 13 cyfr, wpisany EAN: [{}] posiada tylko {} znaków'.format(ean, l)
    checksum_digit = int(ean[-1])
    checksum = 0
    i = 0
    while i != (l - 1):
        checksum += int(ean[i]) * int(EAN_WEIGHTS[i])
        i += 1
    checksum = 10 - checksum % 10
    if checksum == 10:
        checksum = 0
    if checksum == checksum_digit:
        return False
    else:
        return 'Niepoprawna suma kontrolna {} != {}'.format(checksum_digit, checksum)
