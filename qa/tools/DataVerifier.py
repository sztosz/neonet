#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-10-11
#
# @author: sztosz@gmail.com

EAN_WEIGHTS = '13131313131313131313131313'

class DataVerifier():
    def __init__(self):
        pass


    @staticmethod
    def ean13(ean):
        ean = str(ean)
        try:
            int(ean)
        except ValueError:
            return ['ERROR', 'Wrong ean, it has to consist only from digits']
        l = len(ean)
        if l != 13:
            return ['ERROR', 'Wrong ean [{}] length = {} instead of 13'.format(ean,l)]
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
            return ['WARNING', 'Wrong checksum {} != {}'.format(checksum_digit, checksum)]
