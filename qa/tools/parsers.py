#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

import xlrd
from xlrd import XLRDError
from qa.models import Commodity
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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

def parse_commodity(excel_file):
    warnings = list()
    errors = list()
    try:
        workbook = xlrd.open_workbook(file_contents=excel_file.read())
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


def damage_reports_export_to_csv(delimiter=';', data=None):
    if not data:
        raise ObjectDoesNotExist
    else:
        lines = []
        for report in data:
            line = ('', unicode(report.date), report.brand, report.commodity.__unicode__(), report.serial,
                    report.detection_time.detection_time, report.category.category, report.comments,
                    report.further_action.further_action, '', '', (report.user.first_name + ' ' + report.user.last_name))

            # REMEMBER TO CHECK IF \n and \r are striped on entry not output
            line = delimiter.join(x for x in line).replace('\n', ' ').replace('\r', '')

            lines.append(line)
        return '\r\n'.join(lines)


