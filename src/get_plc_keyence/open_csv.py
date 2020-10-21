#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import csv

# read csv file in path
def open_csv(file_path, encoding):
    result = []
    with open(file_path, 'r', newline='', encoding=encoding) as f:
        for row in csv.reader(f):
            result.append(row)
    return result

