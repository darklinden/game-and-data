#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import csv
import numpy as np

__dirname__ = os.path.dirname(os.path.abspath(__file__))


def read_player_prop_reinforce_cost():

    csv_dir = os.getenv('CSV_DIR')
    player_special_reinforce_csv = os.path.join(
        csv_dir, 'PlayerPropReinforceCostTable.csv')

    header = []
    data = []

    with open(player_special_reinforce_csv, 'r', encoding='utf-8') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        # 跳过注释行获取表头
        line = next(spamreader)
        while len(line) == 0 or line[0].startswith('#'):
            line = next(spamreader)

        origin_header = line

        # parse header
        for h in origin_header:

            h = h.strip()
            if len(h) == 0:
                header.append(None)
                continue

            # 跳过注释列
            if h.startswith('#'):
                header.append(None)
                continue

            hl = h.split('|')
            key_type = hl[1].split(':')

            header.append({
                'key': key_type[0].strip(),
                'type': key_type[1].strip()
            })

        for row in spamreader:

            # 跳过空行
            if len(row) == 0 or len(row[0].strip()) == 0:
                continue

            o = {}
            for i in range(len(header)):
                h = header[i]

                # 如果表头为空, 跳过
                if h is None:
                    continue

                d = row[i].strip()
                if len(d) == 0:
                    if h['type'] == 'int32' or h['type'] == 'int64':
                        d = 0
                    elif h['type'] == 'string':
                        d = ''
                else:
                    if h['type'] == 'int32' or h['type'] == 'int64':
                        d = int(d)
                    elif h['type'] == 'string':
                        d = d
                o[h['key']] = d
            data.append(o)

        data = sorted(data, key=lambda x: x['level'])

    return data


def main():

    data = read_player_prop_reinforce_cost()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
