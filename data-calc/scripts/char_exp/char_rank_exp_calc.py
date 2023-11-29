#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse
import os
import sys
import json
import numpy as np

from scripts.plot_tool.curve_plot_power import power_curve_y
from scripts.plot_tool.curve_plot import CurvePlot
from scripts.readers.read_enemy_rank_drop_exp import read_enemy_rank_drop_exp

# 使用次方曲线来计算 升级所需击杀基础怪物个数
# 使用 基础怪物经验值 和 升级所需击杀基础怪物个数 计算出 升级所需经验值


def get_json_save_path():
    # replace current file extension with .json
    abs_file_path = os.path.abspath(__file__)
    abs_file_path = os.path.splitext(abs_file_path)[0]
    return abs_file_path + '.json'


def main():

    # json 存档
    json_save = get_json_save_path()

    # 导出 csv 路径
    csv_dir = os.getenv('CSV_DIR')
    output_csv = os.path.join(csv_dir, 'PlayerCharacterRankExpTable.csv')

    # 基础怪物经验值
    exp_monster = read_enemy_rank_drop_exp()

    # y 为升级所需击杀基础怪物个数
    y_min = 0
    y_max = 100000

    param = 1.41

    # 假设等级下限为 1
    rank_min = 1

    # 假设等级上限为 100
    rank_count = 100

    if os.path.exists(json_save):
        with open(json_save, 'r', encoding='utf-8') as f:
            data = json.load(f)

        rank_count = data['rank_count']
        y_min = data['y_min']
        y_max = data['y_max']
        param = data['param']

    print('rank_min: ', rank_min)
    print('rank_count: ', rank_count)

    # 99 级
    ranks = np.linspace(rank_min, rank_min + rank_count - 1, num=rank_count)

    param_min = -10.0
    param_max = 10.0

    p = CurvePlot(power_curve_y, "char_rank_exp_calc")
    p.set_x(ranks, "rank_count")
    p.set_y(y_min, y_max, "base mon kills")
    p.set_param_range(param_min, param_max, 0.001, param)

    def current_param_callback(data):

        x = data['x']
        y_min = data['y_min']
        y_max = data['y_max']
        param = data['param']
        y = data['y']

        print('y_min: ', y_min)
        print('y_max: ', y_max)
        print('param: ', param)

        with open(json_save, 'w', encoding='utf-8') as f:
            json.dump({
                'rank_count': len(x),
                'y_min': y_min,
                'y_max': y_max,
                'param': param,
            }, f, indent=4)

        if os.path.exists(output_csv) == False:
            print('table not exist: ', output_csv)

        with open(output_csv, 'w', encoding='utf-8') as f:

            # 表头
            print(
                '等级|rank:int32',
                '升级经验|exp:int64',
                '总经验阶段|total_from:int64',
                '总经验阶段|total_to:int64',
                '#基础杀怪经验',
                '#基础杀怪数', sep=',', file=f)

            exp_sum = 0
            for i in range(len(y)):
                monster_count = y[i]
                monster_exp = exp_monster[x[i]]
                exp = monster_count * monster_exp
                exp_sum += exp
                if i == len(y) - 1:
                    # 最后一行标注停止升级
                    print(
                        int(x[i]),
                        int(-1),
                        int(-1),
                        int(-1),
                        "", sep=',', file=f)
                else:
                    print(
                        int(x[i]),
                        int(exp),
                        int(exp_sum),
                        int(monster_exp),
                        int(monster_count),
                        "", sep=',', file=f)

    p.set_current_param_callback(current_param_callback)
    p.show()


if __name__ == '__main__':

    print("""
    计算角色升级所需经验值
    x 轴为等级 y 轴为升级所需杀最小怪物数
    假设最小怪物每个提供 10 经验
    使用次方曲线来计算 升级所需击杀基础怪物个数
    写出到 PlayerCharacterRankExpTable.csv
    """)

    main()