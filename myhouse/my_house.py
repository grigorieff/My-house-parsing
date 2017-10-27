#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re


class UrlError(Exception):
    pass


class Soup:

    def __init__(self, url):
        self.url = url
        self.check_url()

    def check_url(self):
        """
        Check if the given url is from www.reformagkh.ru
        """

        base = 'https://www.reformagkh.ru/myhouse/profile/view/'

        if base not in self.url:
            raise UrlError('It is not an www.reformagkh.ru link. '
                           'Please try the correct link.')

    def get_soup(self):
        """
        Get the soup variable for parsing the passport of a certain house
        """
        page = get(self.url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'lxml')
            return soup
        else:
            raise ConnectionError('The page is not disponible.')


class AllTables(Soup):

    def __init__(self, url):
        super().__init__(url)
        self.soup = self.get_soup()

    def get_table(self):
        """
        Get passport tables
        """
        table_big = self.soup.findAll(class_='subtab')

        return table_big


class FirstTwoTables(AllTables):

    def __init__(self, url):
        super().__init__(url)
        self.big_table = self.get_table()

    def get_lr_context(self):
        """
        Get tables 1 and 2
        """
        all_list = []

        for element in self.big_table[:3]:
            for all_element in element.\
                    select('.col_list > tbody > tr > td > span'):
                all_list.append(all_element.text)

        return all_list

    def clean_lr_context(self):
        """
        Clean left and right sides from junk
        """

        clean_all_list = []

        all_list = self.get_lr_context()

        for element in all_list:
            if ':' in element:
                all_list.remove(element)

        for element in all_list:
            element = element.replace('\n', '')
            clean_all_list.append(element)

        return clean_all_list

    def create_lr_lists(self):
        """
        Create left and right lists
        """
        results = self.clean_lr_context()

        if len(results) % 2 == 0:
            left_list = results[1::2]
            right_list = results[0::2]

            return left_list, right_list
        else:
            raise ArithmeticError('List is not odd, something went wrong.')


class LiftTable(AllTables):

    def __init__(self, url):
        super().__init__(url)
        self.big_table = self.get_table()

    def get_lift_rows(self):
        """
        Get data from table 4, which contains data about lifts
        """
        lift_rows = []

        for element in self.big_table[3].find_all('tr'):
            td_s = element.find_all('td')
            row = [i.text for i in td_s]
            lift_rows.append(row)

        return lift_rows


class PassportTables(LiftTable, FirstTwoTables):

    def __init__(self, url, write=False):
        super().__init__(url)
        self.write = write
        self.write_file()

    def create_df(self):
        """
        Create pandas dataframe
        """
        right_list, left_list = self.create_lr_lists()

        lift_rows = self.get_lift_rows()

        rl_dict = {"right": right_list, "left": left_list}
        rl_df = pd.DataFrame(rl_dict,
                             columns=["left", "right"])

        lift_df = pd.DataFrame(lift_rows[1:len(lift_rows)],
                               columns=['Номер лифта',
                                        'Номер подъезда',
                                        'Тип лифта',
                                        'Год ввода в эксплатацию'])\
            .set_index('Номер лифта')

        return rl_df, lift_df

    def write_file(self):
        """
        If write is True write to file with certain name
        """
        rl_df, lift_df = self.create_df()

        number = re.findall('\d+', self.url)[0]

        if self.write is True:
            with open('house_{}.csv'.format(number), 'w',
                      encoding='utf-8-sig') as file:
                rl_df.to_csv(file, sep=';')
            with open('house_lifts_{}.csv'.format(number), 'w',
                      encoding='utf-8-sig') as file2:
                lift_df.to_csv(file2, sep=';')

    def __str__(self):
        return '{}'.format(self.create_df())

    __repr__ = __str__
