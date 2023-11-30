#!/usr/bin/env python3
# -*- coding: utf8 -*-

import math
from matplotlib import get_backend
import matplotlib.pyplot as plt
import numpy as np

from scripts.util import tab_str
from scripts.readers.parameters import PROJ_COUNT_1_SKILLS, OPERATION_DIFFICULTY_WEIGHT_EASY, OPERATION_DIFFICULTY_WEIGHT_HARD
from scripts.readers.read_skills import merge_features, parse_skill_id, read_skills
from scripts.readers.read_base_stat_prop_type_info import read_base_stat_prop_type_info
from scripts.readers.read_projectiles import read_projectiles
from scripts.readers.read_skill_type_info import read_skill_type_info


def calc_features_to_value(features, base_stat_prop_type_info) -> dict:

    # 属性计算字典 {属性类型: {计算轮序: {属性值类型: 属性值}}}
    feature_dict: dict[str, dict[str, dict[str, float]]] = {}

    # 转换属性列表为计算字典
    for feature in features:
        # 属性类型
        prop_type = feature['prop_type']
        # 属性值
        prop_value = feature['prop_value']
        # 属性值类型
        value_type = feature['value_type']
        # 计算轮序
        calc_order = feature['calc_order']

        # 使用属性类型作为key
        if prop_type not in feature_dict:
            feature_dict[prop_type] = {}

        # 计算轮序
        if calc_order not in feature_dict[prop_type]:
            feature_dict[prop_type][calc_order] = {}

        # 使用属性值类型作为key
        if value_type not in feature_dict[prop_type][calc_order]:
            feature_dict[prop_type][calc_order][value_type] = 0.0

        # 累加属性值
        feature_dict[prop_type][calc_order][value_type] += prop_value

    prop_types = list(feature_dict.keys())
    prop_types.sort()

    value_dict = {}

    for prop_type in prop_types:

        # 多轮计算
        order_type_value_dict = feature_dict[prop_type]

        # 计算轮序
        calc_orders = list(order_type_value_dict.keys())
        calc_orders.sort(key=lambda x: int(x))  # 从小到大

        value = value_dict.get(prop_type, 0.0)
        val_precision = base_stat_prop_type_info[prop_type]['VAL']
        mul_precision = base_stat_prop_type_info[prop_type]['MUL']

        for calc_order in calc_orders:

            type_value_dict = order_type_value_dict[calc_order]

            val_value = type_value_dict.get('VAL', 0.0)
            val_value /= float(val_precision)
            value += val_value

            if mul_precision > 0:
                mul_value = type_value_dict.get('MUL', 0.0)
                mul_value /= float(mul_precision)
                value *= 1.0 + mul_value

            value_dict[prop_type] = value

    return value_dict


def projectile_calc_hit_area(projectile, cd_dec_bonus, proj_dur_bonus, proj_hit_count, move_speed_bonus=1.0):

    dmg_reset_interval = 0
    if projectile['dmg_reset_interval'] > 0:
        dmg_reset_interval = (
            projectile['dmg_reset_interval'] / 1000.0) * cd_dec_bonus

    max_life_time = 0
    if projectile['max_life_time'] > 0:
        max_life_time = projectile['max_life_time'] / 1000.0 * proj_dur_bonus

    move_speed = 0
    if projectile['speeds'][0] > 0:
        move_speed = projectile['speeds'][0] / 1000.0 * move_speed_bonus

    # 简化移动划过的面积 为 矩形
    # 子弹移动距离 = 子弹速度 * 子弹生命周期
    # 子弹划过面积 = (子弹半径 + 子弹移动距离 + 子弹半径) * 子弹半径 * 2

    life_time = dmg_reset_interval if dmg_reset_interval > 0 else max_life_time
    move_length = move_speed * life_time

    collider_radius = projectile['circle_colliders'] / 1000.0

    hit_area = (collider_radius + move_length +
                collider_radius) * collider_radius * 2
    hit_count = round(hit_area)

    print('projectile', projectile['projectile_type'],
          'hit_count', hit_count, 'proj_hit_count', proj_hit_count)
    return hit_count if proj_hit_count > hit_count else proj_hit_count


def calc_skill_dps(skill, projectiles_data, base_stat_prop_type_info, passive):

    # 计算技能属性值
    features = merge_features(skill['features'], passive)
    # print('features', json.dumps(features, indent=4))

    features_value = calc_features_to_value(features, base_stat_prop_type_info)
    # print('features_value', json.dumps(features_value, indent=4))

    # 计算技能伤害

    projectiles = []
    projectile_ids = skill['projectiles']
    for projectile_id in projectile_ids:
        projectile = projectiles_data[projectile_id]
        projectiles.append(projectile)

    # 当前技能 属性值
    # 攻击强度
    atk = features_value.get('Atk', 0.0)
    # 冷却缩减
    cd_dec_bonus = 1.0 - features_value.get('CDDecBonus', 0)
    # 投射物生成数 = 角色估定属性1 + 投射物数强化
    proj_count = 1 + features_value.get('ProjCountBonus', 0)
    # 投射物速度强化 = 投射物速度 * (1 + 投射物速度强化)
    proj_speed_bonus = 1.0 + features_value.get('ProjSpeedBonus', 0)
    # 投射物持续时间强化 = 角色估定属性1 + 投射物持续时间强化
    proj_dur_bonus = 1.0 + features_value.get('ProjDurBonus', 0)
    # 投射物穿透强化 = 角色估定属性1 + 投射物穿透强化
    proj_hit_count = 1 + features_value.get('ProjHitCountBonus', 0)

    print(
        skill['skill_type'],
        'atk', atk,
        'proj_count', proj_count,
        'proj_hit_count', proj_hit_count)

    dps = 0.0
    # 无投射物 的 和 会产生子投射物的技能需要特殊处理
    # 计算的是极限 dps 假设每个投射物都能攻击到有效目标
    if skill['skill_type'] == 'Skill3':

        # 闪电链 无投射物
        # 造成伤害数 =
        total_hit_count = proj_count
        # 时长 = cd时间
        cd_time = (skill['cooldown'] / 1000.0) * cd_dec_bonus
        dps = atk * total_hit_count / cd_time

    elif len(projectiles) == 1:
        # 无子投射物

        p = projectiles[0]
        hit_count = projectile_calc_hit_area(
            p, cd_dec_bonus, proj_dur_bonus, proj_hit_count, proj_speed_bonus)

        if skill['cooldown'] > 0:
            # 有冷却时间 计算总伤害 / 冷却时间

            if p['dmg_reset_interval'] > 0:
                # 单投射物生存时间 = 投射物持续时间 * 投射物持续时间强化
                des_life_time = p['max_life_time'] / 1000.0 * proj_dur_bonus
                # 有伤害重置间隔
                des_dmg_reset_interval = p['dmg_reset_interval'] / \
                    1000.0 * cd_dec_bonus
                # 伤害产生数 = 个数 * 穿透数 * 时间 / 重置间隔
                des_dmg_count = proj_count * hit_count * \
                    max(math.floor(des_life_time / des_dmg_reset_interval), 1)
            else:
                # 无伤害重置间隔
                des_dmg_count = proj_count * hit_count

            # 单次伤害 = 攻击强度 * 伤害转化率 * 数量
            total_damage = atk * (p['damage'] / 1000.0) * des_dmg_count
            cd_time = (skill['cooldown'] / 1000.0) * cd_dec_bonus
            dps = total_damage / cd_time

        else:
            # 无冷却时间

            # 有伤害重置间隔
            des_dmg_reset_interval = p['dmg_reset_interval'] / \
                1000.0 * cd_dec_bonus

            if skill['skill_type'] == 'HolyImpact_Out':
                des_dmg_reset_interval = float(
                    skill['other_cast_params'].strip())

            if des_dmg_reset_interval > 0:

                if skill['skill_type'] in PROJ_COUNT_1_SKILLS:
                    proj_count = 1

                # 伤害产生数 = 个数 * 穿透数 * 时间 / 重置间隔
                des_dmg_count = proj_count * hit_count

                # 单次伤害 = 攻击强度 * 伤害转化率 * 数量
                total_damage = atk * (p['damage'] / 1000.0) * des_dmg_count
                cd_time = des_dmg_reset_interval
                dps = total_damage / cd_time

            else:
                raise Exception('无冷却时间且无伤害重置间隔', skill['skill_type'])

    else:
        raise Exception('技能不支持: ' + skill['skill_type'])

    return dps


def main():

    # 读取技能数据
    skills_data = read_skills()
    # 读取投射物数据
    projectiles_data = read_projectiles()
    # 读取基础属性类型信息
    base_stat_prop_type_info = read_base_stat_prop_type_info()
    # 读取技能类型信息
    skill_type_info = read_skill_type_info()

    skill_ids = list(skills_data.keys())

    skill_ids.sort(key=lambda x: int(x))

    skill_tag_list = []
    dps_list = []
    dps_with_difficulty_list = []

    base_data = [{'prop_type': 'Atk', 'prop_value': 100,
                  'value_type': 'VAL', 'calc_order': 0}]

    # 拆分每个技能的每个等级每种投射物的 dps
    for skill_id in skill_ids:
        skill = skills_data[skill_id]
        skill_dps = calc_skill_dps(
            skill, projectiles_data, base_stat_prop_type_info, base_data)

        _, skill_level = parse_skill_id(skill_id)
        skill_type = skill['skill_type']
        skill_tag = skill_type + '-' + str(skill_level)

        skill_type_info_data = skill_type_info[skill_type]
        difficulty = skill_type_info_data['operation_difficulty']
        # 难度系数 100 为无难度 1000 为最高难度
        # 难度系数直接影响 dps 分值, 系数 map 为 0 ~ 1000 -> 1.4 ~ 0.6
        factor = difficulty / 1000.0 * (OPERATION_DIFFICULTY_WEIGHT_HARD - OPERATION_DIFFICULTY_WEIGHT_EASY) + \
            OPERATION_DIFFICULTY_WEIGHT_EASY

        skill_tag_list.append(skill_tag)
        dps_list.append(skill_dps)
        dps_with_difficulty_list.append(skill_dps * factor)

        print('skill: ' + tab_str(skill_type) + '\tdps: ' +
              tab_str(skill_dps) + '\tscore: ' + str(factor))

    f0 = plt.figure('skill dps')

    # Set position of bar on X axis
    barWidth = 0.2
    base = np.arange(len(skill_tag_list))
    br1 = [x - barWidth for x in base]
    br2 = [x + barWidth for x in base]

    # Make the plot
    plt.bar(br1, dps_list, color='r', width=barWidth,
            edgecolor='grey', label='dps')
    plt.bar(br2, dps_with_difficulty_list, color='g', width=barWidth,
            edgecolor='grey', label='dps with difficulty')

    plt.xticks([r for r in range(len(skill_tag_list))], skill_tag_list)

    plt.show()


if __name__ == '__main__':

    print(""" 
# 计算技能的伤害偏好, 生成柱状图
# 技能的CD和持续时间差异很大，但是持续时间不会超过CD，
# 可以把长CD技能看作是伤害重置间隔较长的永久技能
# 那么计算技能极限DPS的时候，永久持续性技能和长CD技能也可以以一个“均值”去计算了
# 对于无CD技能, 极限DPS = 伤害重置间隔的伤害 * 投射物个数 * 每个投射物可伤害次数 / 伤害重置间隔时间
# 对于有CD技能, 极限DPS = 单次技能施放周期总伤害 * 投射物个数 * 每个投射物可伤害次数 / CD时间

# 有飞行速度或飞行速度较快的投射物 一般 每个投射物可伤害次数 的影响大于 伤害重置间隔 (一般较少攻击到同一目标)
# 无飞行速度或飞行速度较慢的投射物 一般 伤害重置间隔 的影响大于 每个投射物可伤害次数 (常见对同一目标多次攻击)

# 已知某个投射物的击中目标概率和其面积与所划过距离正相关
# 这个相关系数影响的是投射物的伤害重置间隔期间的伤害个数
# 因为单怪大概占地面积约为1, 那么使用投射物面积 * 单伤害重置间隔划过距离 就可以得到伤害重置间隔期间 伤害大约个数
# 如果 投射物穿透 大于 伤害大约个数, 那么就是 伤害大约个数 否则 就是 投射物穿透
# 伤害重置间隔期间 伤害大约个数 * 投射物生命周期 / 伤害重置间隔 就是 总伤害分数
# 这一系列操作只会将 伤害重置间隔期间的伤害个数 转换为 一个更加精确的伤害分数 这个分数是一个理论上的极限值，因为实际游戏中怪物并不是均匀平铺在地面上的
    
    """)

    main()
