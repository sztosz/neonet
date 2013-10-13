#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

import xlrd
from qa.tools.DataVerifier import DataVerifier
from qa.models import Commodity

class ExcelParser():
    def __init__(self):
        pass

    @staticmethod
    def parse_commodity(excel_file):
        workbook = xlrd.open_workbook(file_contents=excel_file.read())
        worksheet = workbook.sheet_by_index(0)
        warnings = list()
        errors = list()
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        if num_cells < 24:
            errors.append('Imported file has too little columns to be valid')
        else:
            curr_row = -1
            while curr_row < num_rows:
                curr_row += 1
                sku = worksheet.cell_value(curr_row, 0)
                name = worksheet.cell_value(curr_row, 1)
                ean = worksheet.cell_value(curr_row, 16)
                ean_is_invalid = DataVerifier.ean13(ean)
                if ean_is_invalid:
                    if ean_is_invalid[0] == 'ERROR':
                        errors.append('ERROR in row {} : {}; NAME: {}'.format(curr_row+1, ean_is_invalid[1], name))
                        continue
                    else:
                        warnings.append('WARNING in row {} : {} NAME: {}'.format(curr_row+1, ean_is_invalid[1], name))
                if Commodity.objects.filter(sku=sku):
                    warnings.append('WARNING in row {}; SKU : {} already in database and was not added'. \
                        format(curr_row + 1, sku))
                else:
                    commodity = Commodity(sku=sku, name=name, ean=ean)
                    commodity.save()

        return warnings, errors
