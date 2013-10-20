#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

from __future__ import unicode_literals

import xlrd
from xlrd import XLRDError
from qa.tools.DataVerifier import DataVerifier
from qa.models import Commodity


class ExcelParser():
    def __init__(self):
        pass

    @staticmethod
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
        if num_cells < 24:
            errors.append('Zbyt mała ilość kolumn, plik posiada niepoprawne dane')
        else:
            curr_row = -1
            while curr_row < num_rows:
                curr_row += 1
                sku = worksheet.cell_value(curr_row, 0)
                name = worksheet.cell_value(curr_row, 1)
                ean = worksheet.cell_value(curr_row, 16)
                ean_is_invalid = DataVerifier.ean13(ean)
                if ean_is_invalid:
                    if ean_is_invalid[0] == 'BŁĄD':
                        errors.append('BŁĄD w lini {} : {}; TOWAR: {}'.format(curr_row+1, ean_is_invalid[1], name))
                        continue
                    else:
                        warnings.append('OSTRZEŻENIE w lini {} : {} TOWAR: {}'.format(curr_row+1, ean_is_invalid[1],
                            name))
                if Commodity.objects.filter(sku=sku):
                    warnings.append('OSTRZEŻENIE w lini {}; TOWAR: {} SKU: {} jest już w '
                        'bazie i towar nie został dodany'.format(curr_row + 1, name, sku))
                else:
                    commodity = Commodity(sku=sku, name=name, ean=ean)
                    commodity.save()

        return warnings, errors

    #@staticmethod
    #def reports_to_excel(self):
    #    wb = workbook.Workbook()
    #    worksheet = wb.get_active_sheet()
