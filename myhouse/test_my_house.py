#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

import unittest
import myhouse.my_house as my_house
from myhouse.my_house import UrlError
# from unittest import mock


class Exceptions(unittest.TestCase):

    def test_check_url(self):
        with self.assertRaises(UrlError) as context:
            my_house.Soup(url='dhfdfhfdhfd')

    def test_validity(self):
        with self.assertRaises(ConnectionError) as context:
            my_house.Soup(url='https://www.reformagkh.ru/m'
                              'yhouse/profile/view/7fddfdfdf463/').get_soup()
