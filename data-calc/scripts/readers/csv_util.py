#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import csv


def read_csv(csv_file_path: str, to_dict_by_key: str = '') -> list or dict:

    header = []
    data_type_is_int = []

    list_data = []
    dict_data = {}

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        isEnum = csv_file_path.endswith('Enum.csv')

        if not isEnum:
            # 跳过注释行 表头为第一行不以#开头的非空行
            line = next(spamreader)
            while len(line) == 0 or len(line[0]) == 0 or line[0].startswith('#'):
                line = next(spamreader)

            origin_header = line

            # parse header
            for h in origin_header:

                h = h.strip()
                if len(h) == 0:
                    header.append(None)
                    data_type_is_int.append(False)
                    continue

                # 跳过注释列
                if h.startswith('#'):
                    header.append(None)
                    data_type_is_int.append(False)
                    continue

                hl = h.split('|')
                key_type = hl[1].split(':')
                key = key_type[0].strip()

                header.append(key)
                dt = key_type[1].strip().startswith('int')
                data_type_is_int.append(dt)

        for row in spamreader:

            # 跳过空行 或 以#开头的注释行
            if len(row) == 0 or len(row[0]) == 0 or row[0].startswith('#'):
                continue

            if isEnum:
                list_data.append(row[0].strip())
            else:
                o = {}
                for i in range(len(header)):
                    h = header[i]

                    # 如果表头为空, 跳过
                    if h is None:
                        continue

                    d = row[i].strip()
                    if data_type_is_int[i]:
                        if d == '' or d == '-1':
                            d = -1
                        else:
                            d = int(d)
                    o[h] = d

                if to_dict_by_key == '':
                    list_data.append(o)
                else:
                    dict_data[o[to_dict_by_key]] = o

    return list_data if to_dict_by_key == '' else dict_data


if __name__ == "__main__":
    # do some test

    print("--------------------")
    print("test csv_util")
    print("--------------------")

    __dirname__ = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.realpath(os.path.join(__dirname__, 'test.csv'))

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    with open(csv_file_path, 'w', encoding='utf-8') as csvfile:
        print("# write test.csv", file=csvfile)
        print("ID|id:int32,Name|name:string", file=csvfile)
        print("1,test1", file=csvfile)
        print("2,test2", file=csvfile)
        print("3,test3", file=csvfile)

    data = read_csv(csv_file_path)
    print(data)

    os.remove(csv_file_path)
