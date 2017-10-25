#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

import unittest
import myhouse.my_house as my_house
from unittest import mock


class TestParserErrors(unittest.TestCase):

    def test_check_url(self):
        with self.assertRaises(ValueError) as context:
            my_house.Tabler(url='dhfdfhfdhfd')

    def test_validity(self):
        with self.assertRaises(ConnectionError) as context:
            my_house.Tabler(url='https://www.reformagkh.ru/myhouse/profile/view/7fddfdfdf463/')


# class TestTablerErrors(unittest.TestCase):
#
#     def
