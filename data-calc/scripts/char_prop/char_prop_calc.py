#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import numpy as np

from scripts.plot_tool.curve_plot_tanh import tanh_curve_y
from scripts.plot_tool.curve_plot import CurvePlot
from scripts.readers.parameters import *
from scripts.readers.read_player_prop_reinforce_cost import read_player_prop_reinforce_cost
from scripts.util import tab_str


def get_json_save_path():
    # replace current file extension with .json
    abs_file_path = os.path.abspath(__file__)
    abs_file_path = os.path.splitext(abs_file_path)[0]
    return abs_file_path + '.json'


def calc_deliver(level_cost_list, level_deliver_list):

    # 属性购买消耗阶梯数组 level_cost_list
    # 属性目标阶梯数组 level_deliver_list
    # 冗余系数 COIN_DELIVER_REDUNDANCY

    # 打印表头
    print(
        tab_str("关卡"),
        tab_str("目标属性值"),
        tab_str("对应金币投放"),
        tab_str("对应金币总投放"),
        tab_str("极限属性值"), sep='')

    # 总金币消耗
    coin_delivers = []
    total_coin_delivers = []

    # 上一关卡的属性值
    pre_level = 0

    for i in range(len(level_deliver_list)):

        # 当前关卡的属性目标值
        to_level = level_deliver_list[i]

        # 当前关卡的属性目标值 不能大于属性可达最大值
        if to_level > len(level_cost_list):
            raise Exception("第", i + 1, "关 属性目标值为：",
                            to_level, "超出属性购买消耗阶梯数组长度")

        # 计算当前关卡的属性购买消耗
        coin_deliver = 0
        for j in range(pre_level, to_level, 1):
            cost = level_cost_list[j]
            # print("第", j + 1, "级 属性购买消耗为：", cost)
            coin_deliver += cost

        # 添加投放冗余
        # 从属性投放计算出金币投放后 为了防止玩家过弱导致无法通关的情况 会对金币投放以一定系数进行补强
        coin_deliver = round(coin_deliver * COIN_DELIVER_REDUNDANCY)
        coin_delivers.append(coin_deliver)

        # 计算当前关卡的总金币消耗
        pre_level_total_coin_deliver = total_coin_delivers[i -
                                                           1] if i > 0 else 0
        total_coin_deliver = coin_deliver + pre_level_total_coin_deliver
        total_coin_delivers.append(total_coin_deliver)

        # 计算极限属性值
        level_upper_limits_deliver = 0
        tmp_coin_deliver = total_coin_deliver
        for j in range(0, len(level_cost_list), 1):
            if j > len(level_cost_list):
                break
            cost = level_cost_list[j]
            if tmp_coin_deliver >= cost:
                tmp_coin_deliver -= cost
                level_upper_limits_deliver += 1
            else:
                break

        print(
            tab_str(str(i + 1)),
            tab_str(str(to_level)),
            tab_str(str(coin_deliver)),
            tab_str(str(total_coin_deliver)),
            tab_str(str(level_upper_limits_deliver)), sep='')

        pre_level = level_deliver_list[i]

    return coin_delivers, total_coin_delivers


def main():

    # 以关卡解锁作为玩家游戏进度的指标
    # DUNGEON_LEVEL_COUNT

    # json 存档
    json_save = get_json_save_path()

    # 从属性购买表中读取数据
    char_prop_buy_calc = read_player_prop_reinforce_cost()

    # 属性等级购买消耗
    prop_level_costs = []
    for i in range(len(char_prop_buy_calc)):
        prop = char_prop_buy_calc[i]
        prop_level_costs.append(prop['cost'])

    prop_level_count = len(prop_level_costs)

    y_min = 0
    y_max = prop_level_count
    param_min = -0.2
    param_max = 0.5
    param = 0.1

    # 读取存档
    if os.path.exists(json_save):
        with open(json_save, 'r', encoding='utf-8') as f:
            data = json.load(f)

        level_count = data['level_count']
        y_min = data['y_min']
        y_max = data['y_max']
        param = data['param']

        if DUNGEON_LEVEL_COUNT != level_count:
            print('level_count not match')

    game_level = np.linspace(1, DUNGEON_LEVEL_COUNT, num=DUNGEON_LEVEL_COUNT)
    p = CurvePlot(tanh_curve_y, "char_prop_calc")
    p.set_x(game_level, "game_level")
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

        pre_value = 0
        level_deliver_list = []
        print(
            tab_str("游戏进度"),
            tab_str("预期属性"),
            tab_str("本节预期属性投放"), sep='')
        for i in range(len(x)):
            g_l = int(x[i])
            p_t = int(y[i])
            level_deliver_list.append(int(p_t))
            prop_diff = p_t - pre_value
            pre_value = p_t
            print(tab_str(str(g_l)), tab_str(str(p_t)),
                  tab_str(str(prop_diff)), sep='')

        print('')
        coin_delivers, total_coin_delivers = calc_deliver(
            prop_level_costs, level_deliver_list)

        print('')

        with open(json_save, 'w', encoding='utf-8') as f:

            dict = {
                'level_count': DUNGEON_LEVEL_COUNT,
                'y_min': y_min,
                'y_max': y_max,
                'param': param,
                'delivers': []
            }

            for i in range(len(x)):
                dict['delivers'].append({
                    'game_level': int(x[i]),
                    'prop_deliver': int(y[i]),
                    'coin_deliver': coin_delivers[i],
                    'total_coin_deliver': total_coin_delivers[i],
                })

            json.dump(dict, f, indent=4)

    p.set_current_param_callback(current_param_callback)
    p.show()


if __name__ == '__main__':

    print(""" 
    读取 PlayerPropReinforceCostTable.csv 中的消耗数据
    x 为 关卡, 代表 游戏进度, y 为 总属性等级, 代表 对应关卡进度下的玩家角色强度
    使用双曲函数平滑每关卡属性等级投放
    使用总属性等级计算每关卡属性等级
    """)

    main()
