#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: Bartosz Nowak sztosz@gmail.com
#
# This file is licensed GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

from __future__ import unicode_literals

from xlrd import XLRDError, open_workbook
from DamageReports.models import Commodity
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def validate_ean13(ean):
    weights = '13131313131313131313131313'
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
        checksum += int(ean[i]) * int(weights[i])
        i += 1
    checksum = 10 - checksum % 10
    if checksum == 10:
        checksum = 0
    if checksum == checksum_digit:
        return False
    else:
        return 'Niepoprawna suma kontrolna {} != {}'.format(checksum_digit, checksum)


def parse_commodity(excel_file):
    warnings = list()
    errors = list()
    try:
        workbook = open_workbook(file_contents=excel_file.read())
    except XLRDError:
        errors.append('Nie można wczytać pliku, prawdopodobnie nie jest to plik excel')
        return warnings, errors
    worksheet = workbook.sheet_by_index(0)
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    if num_cells < 3:
        errors.append('Zbyt mała ilość kolumn, plik posiada niepoprawne dane')
    else:
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            sku = worksheet.cell_value(curr_row, 1)
            name = worksheet.cell_value(curr_row, 2)
            ean = worksheet.cell_value(curr_row, 0)
            ean_is_invalid = validate_ean13(ean)
            if ean_is_invalid:
                continue
            try:
                commodity = Commodity.objects.get(ean=ean)
            except ObjectDoesNotExist:
                commodity = Commodity(sku=sku, name=name, ean=ean)
                commodity.save()
            except MultipleObjectsReturned:
                errors.append('BŁĄD w lini {} jest już wpisany do bazy kilkukrotnie'.format(curr_row + 1))
            if commodity.name == 'BRAK_TOWARU_W_BAZIE':
                commodity.name = name
                commodity.save()
                warnings.append('OSTRZEŻENIE w lini {}; TOWAR z EAN\'em {} dostał poprawną nazwę: '
                                '{}'.format(curr_row + 1, ean, name))
    return warnings, errors

