#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import csv
from scripts.readers.csv_util import read_csv

__dirname__ = os.path.dirname(os.path.abspath(__file__))


# 读取基础属性类型信息
def read_base_stat_prop_type_info():

    csv_dir = os.environ.get('CSV_DIR')
    base_stat_prop_type_info_csv = os.path.join(
        csv_dir, 'BaseStatPropTypeInfoTable.csv')

    data = read_csv(base_stat_prop_type_info_csv, 'prop_type')

    for prop_type in data:

        d = data[prop_type]

        # 加值精度
        val_precision = d['val_precision']
        d['VAL'] = int(val_precision)
        del d['val_precision']

        # 乘值精度
        mul_precision = d['mul_precision']
        d['MUL'] = int(mul_precision)
        del d['mul_precision']

    return data


def main():

    data = read_base_stat_prop_type_info()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
