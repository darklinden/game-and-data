#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import json
import numpy as np

from scripts.readers.parameters import PLAYER_PROP_COUNT
from scripts.plot_tool.curve_plot import CurvePlot
from scripts.plot_tool.curve_plot_power import power_curve_y
from scripts.util import tab_str


def get_json_save_path():
    # replace current file extension with .json
    abs_file_path = os.path.abspath(__file__)
    abs_file_path = os.path.splitext(abs_file_path)[0]
    return abs_file_path + '.json'


def main():

    csv_dir = os.getenv('CSV_DIR')
    json_save = get_json_save_path()

    print('prop_count: ', PLAYER_PROP_COUNT)

    y_min = 0
    y_max = 100000
    param_min = -10.0
    param_max = 10.0
    param = 1.0

    if os.path.exists(json_save):
        with open(json_save, 'r', encoding='utf-8') as f:
            data = json.load(f)

        level_count = data['level_count']
        y_min = data['y_min']
        y_max = data['y_max']
        param = data['param']

        if level_count != PLAYER_PROP_COUNT:
            print('level_count not match')

    prop_level = np.linspace(1, PLAYER_PROP_COUNT, num=PLAYER_PROP_COUNT)
    p = CurvePlot(power_curve_y, "char_prop_buy_calc")
    p.set_x(prop_level, "prop_level")
    p.set_y(y_min, y_max, "y")
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

        print(tab_str('属性等级'), tab_str('本阶购买消耗'), tab_str('总消耗'), sep='')
        sum_value = 0
        for i in range(len(y)):
            c = int(y[i])
            sum_value += c
            print(tab_str(int(x[i])), tab_str(c), tab_str(sum_value), sep='')

        with open(json_save, 'w', encoding='utf-8') as f:
            json.dump({
                'level_count': PLAYER_PROP_COUNT,
                'y_min': y_min,
                'y_max': y_max,
                'param': param,
            }, f, indent=4)

        prop_level_cost_list = y

        # 导出属性购买消耗配置
        player_prop_reinforce_cost_csv = os.path.join(
            csv_dir, 'PlayerPropReinforceCostTable.csv')
        with open(player_prop_reinforce_cost_csv, 'w', encoding='utf-8') as f:
            print('属性等级|level:int32,本阶购买消耗|cost:int32,总消耗|total:int32', file=f)

            cost_sum = 0
            for i in range(len(prop_level_cost_list)):
                cost = int(prop_level_cost_list[i])
                cost_sum += cost

                print(i + 1, cost, cost_sum, sep=',', file=f)

        print('write_player_prop_reinforce_cost done')

    p.set_current_param_callback(current_param_callback)
    p.show()


if __name__ == '__main__':

    print("""
    x 为 属性等级, y 为 当拥有 x-1 级属性时，升级到 x 级属性所需的金币
    使用次方曲线计算每级升级所需金币
    生成 char_prop_buy_calc.json
    生成 PlayerPropReinforceCostTable.csv
    """)

    main()
