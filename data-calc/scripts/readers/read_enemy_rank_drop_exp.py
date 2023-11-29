#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import json
from scripts.readers.csv_util import read_csv

# 读取等级对应怪物掉落经验值


def read_enemy_rank_drop_exp():

    csv_dir = os.getenv('CSV_DIR')
    base_stat_prop_type_info_csv = os.path.join(
        csv_dir, 'EnemyRankDropExpTable.csv')

    data = read_csv(base_stat_prop_type_info_csv)

    dict_data = {}
    for d in data:

        rank = int(d['rank'])
        exp = int(d['exp'])

        dict_data[rank] = exp

    return dict_data


def main():

    data = read_enemy_rank_drop_exp()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
