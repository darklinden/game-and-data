#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import csv

__dirname__ = os.path.dirname(os.path.abspath(__file__))
__parent_dirname__ = os.path.dirname(__dirname__)

from scripts.readers.csv_util import read_csv


def read_projectile(csv_file_path):

    header = []
    data = {}

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        origin_header = next(spamreader)

        # parse header
        for h in origin_header:

            if h.strip() == '':
                header.append(None)
                continue

            # 跳过注释行
            if h.startswith('#'):
                header.append(None)
                continue

            hl = h.split('|')
            key_type = hl[1].split(':')
            key = key_type[0].strip()

            # 跳过粒子效果配置
            if key.startswith('particle_'):
                header.append(None)
                continue

            # 虽然支持多个圆形碰撞 和 多个长方形碰撞, 但是目前测试过程中发现只有一个圆形碰撞就可以满足需求 暂时先这么处理

            # 跳过 长方形碰撞
            if key in ['line_colliders']:
                header.append(None)
                continue

            header.append(key)

        for row in spamreader:

            # 跳过空行
            if len(row[0].strip()) == 0:
                continue

            o = {}
            for i in range(len(header)):
                h = header[i]

                # 如果表头为空, 跳过
                if h is None:
                    continue

                # 将圆形碰撞简化 存储 为一个圆形半径
                if h in ['circle_colliders']:
                    v_str = row[i].strip()
                    if v_str == '':
                        o[h] = 0
                        continue

                    collider_radius = v_str.strip(';')
                    collider_radius = collider_radius.split('#')[2]
                    collider_radius = collider_radius.strip()
                    o[h] = float(collider_radius) / 1000.0
                    continue

                # 速度
                if h in ['speeds']:
                    v_str = row[i].strip()
                    if v_str == '':
                        o[h] = []
                        continue

                    v_str = v_str.strip(';')
                    v = v_str.split(';')
                    o[h] = []
                    for vv in v:
                        vv = vv.strip()
                        if vv == '':
                            continue
                        o[h].append(float(vv) / 1000.0)
                    continue

                # 精度
                if h in ['dmg_delay', 'dmg_reset_interval', 'damage', 'knock', 'max_life_time']:
                    v_str = row[i].strip()
                    if v_str == '' or v_str == '-1':
                        o[h] = -1
                        continue

                    o[h] = (float(v_str) / 1000.0)
                    continue

                o[h] = row[i]

            data[o['projectile_type']] = o

    return data, header


def read_projectiles():

    csv_dir = os.environ.get('CSV_DIR')
    projectiles_csv = os.path.join(csv_dir, 'ProjectilesTable.csv')

    data = read_csv(projectiles_csv, 'projectile_type')

    for projectile_id in data:
        d = data[projectile_id]

        # 将圆形碰撞简化 存储 为一个圆形半径
        if 'circle_colliders' in d:
            v_str = d['circle_colliders']
            if v_str == '':
                d['circle_colliders'] = 0
            else:
                collider_radius = v_str.strip(';')
                collider_radius = collider_radius.split('#')[2]
                collider_radius = collider_radius.strip()
                d['circle_colliders'] = int(collider_radius)

        # 速度
        if 'speeds' in d:
            v_str = d['speeds']
            if v_str == '':
                d['speeds'] = []
            else:
                v_str = v_str.strip(';')
                v = v_str.split(';')
                d['speeds'] = []
                for vv in v:
                    vv = vv.strip()
                    if vv == '':
                        continue
                    d['speeds'].append(int(vv))

        # 精度
        if 'dmg_delay' in d:
            v_str = d['dmg_delay']
            if v_str == '' or v_str == '-1':
                d['dmg_delay'] = -1
            else:
                d['dmg_delay'] = int(v_str)

        if 'dmg_reset_interval' in d:
            v_str = d['dmg_reset_interval']
            if v_str == '' or v_str == '-1':
                d['dmg_reset_interval'] = -1
            else:
                d['dmg_reset_interval'] = int(v_str)

        if 'damage' in d:
            v_str = d['damage']
            if v_str == '' or v_str == '-1':
                d['damage'] = -1
            else:
                d['damage'] = int(v_str)

        if 'knock' in d:
            v_str = d['knock']
            if v_str == '' or v_str == '-1':
                d['knock'] = -1
            else:
                d['knock'] = int(v_str)

        if 'max_life_time' in d:
            v_str = d['max_life_time']
            if v_str == '' or v_str == '-1':
                d['max_life_time'] = -1
            else:
                d['max_life_time'] = int(v_str)

    return data


def main():

    data = read_projectiles()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
