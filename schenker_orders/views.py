#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on 2013-11-29
#
# @author: sztosz@gmail.com

from neonet.views import AbstractView


class Order(AbstractView):
    def _place(self):
        pass

    def _show(self):
        pass

    def _change(self):
        pass

    def _add_to_list(self):
        pass

    def _view(self):
        pass


class OrderList(AbstractView):
    def create(self):
        pass

    def _show(self):
        pass

    def _view(self):
        pass

    def _export(self):
        pass


