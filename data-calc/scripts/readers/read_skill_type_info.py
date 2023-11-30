#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import csv

__dirname__ = os.path.dirname(os.path.abspath(__file__))
__parent_dirname__ = os.path.dirname(__dirname__)

from scripts.readers.csv_util import read_csv


def read_skill_type_info():

    csv_dir = os.environ.get('CSV_DIR')
    skill_type_info_csv = os.path.join(csv_dir, 'SkillTypeInfoTable.csv')

    data = read_csv(skill_type_info_csv, 'skill_type')

    # buff 特殊处理
    for eot_id in data:
        d = data[eot_id]

        if 'operation_difficulty' in d:
            if d['operation_difficulty'] == '':
                d['operation_difficulty'] = 0
            else:
                d['operation_difficulty'] = int(d['operation_difficulty'])

        if 'skill_detect_refresh' in d:
            if d['skill_detect_refresh'] == '':
                d['skill_detect_refresh'] = []
            else:
                d['skill_detect_refresh'] = d['skill_detect_refresh'].split(
                    ';')

        if 'passive_not_affected' in d:
            if d['passive_not_affected'] == '':
                d['passive_not_affected'] = []
            else:
                d['passive_not_affected'] = d['passive_not_affected'].split(
                    ';')

    return data


def main():

    data = read_skill_type_info()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
