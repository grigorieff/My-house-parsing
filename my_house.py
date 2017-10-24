#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Alexey Koshevoy

from requests import get
from bs4 import BeautifulSoup
import pandas as pd


class Parser:

    def __init__(self, url):
        self.url = url
        self.check_url()

    def check_url(self):
        """
        check if the given url is from www.reformagkh.ru
        !!!add if something with connection!!!
        """

        base = 'https://www.reformagkh.ru/myhouse/profile/view/'

        if base not in self.url:
            raise ValueError('It is not an www.reformagkh.ru link. Please try the correct link.')

    def get_soup(self):
        """
        get the soup variable for parsing the passport of a certain house.
        """
        page = get(self.url)
        soup = BeautifulSoup(page.text, 'lxml')
        return soup

    def get_table(self):
        """
        get passport tables
        """

        soup = self.get_soup()
        table_big = soup.findAll(class_='subtab')

        return table_big

    def get_lr_context(self):
        """
        get all context and 4 and 5, which are tables
        """
        all_list = []

        for element in self.get_table()[:3]:
            for all_element in element.select('.col_list > tbody > tr > td > span'):
                all_list.append(all_element.text)

        return all_list

    def get_lift_rows(self):
        """
        Here I get the data from table 4
        """
        lift_rows = []

        for element in self.get_table()[3].find_all('tr'):  # parse the 4-th table
            td_s = element.find_all('td')
            row = [i.text for i in td_s]
            lift_rows.append(row)

        return lift_rows

    def clean_lr_context(self):
        """
        clean lr context from useless shit
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


class Tabler(Parser):

    def __init__(self, url, write=False):
        Parser.__init__(self, url)
        self.write = write
        self.write_file()

    def create_lr_lists(self):
        """
        create left and right lists
        """
        results = Parser.clean_lr_context(self)

        if len(results) % 2 == 0:
            left_list = results[1::2]
            right_list = results[0::2]

            return left_list, right_list
        else:
            raise ArithmeticError('List is not odd, something went wrong.')

    def create_df(self):
        """
        create pandas dataframe
        """
        right_list, left_list = self.create_lr_lists()

        lift_rows = self.get_lift_rows()

        rl_dict = {"right": right_list, "left": left_list}
        rl_df = pd.DataFrame(rl_dict, columns=["left", "right"])

        lift_df = pd.DataFrame(lift_rows[1:len(lift_rows)], columns=['Номер лифта','Номер подъезда',
                                                                     'Тип лифта', 'Год ввода в эксплатацию'])\
            .set_index('Номер лифта')

        return rl_df, lift_df

    def write_file(self):
        """
        if write is True write to file
        """
        rl_df, lift_df = self.create_df()

        if self.write is True:
            with open('house123.csv', 'w', encoding='utf-8-sig') as file:
                rl_df.to_csv(file, sep=';')
            with open('house4.csv', 'w', encoding='utf-8-sig') as file2:
                lift_df.to_csv(file2, sep=';')

    def __str__(self):
        return '{}'.format(self.create_df())

    __repr__ = __str__


# def call(url, write=False):
    # inst = Tabler(url='https://www.reformagkh.ru/myhouse/profile/view/7628463/', write=write)
    # print(inst)

inst = Tabler(url='https://www.reformagkh.ru/myhouse/profile/view/7628463/', write=True)
print(inst)