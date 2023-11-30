#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import json

__dirname__ = os.path.dirname(os.path.abspath(__file__))

from scripts.readers.csv_util import read_csv


def parse_feature(features_str):
    feature = features_str.split('#')
    ff = {}
    ff['prop_type'] = feature[0]
    ff['prop_value'] = int(feature[1])
    ff['value_type'] = feature[2]
    ff['calc_order'] = int(feature[3])
    return ff


def parse_features(features_str):
    features_strs = features_str.split(';')
    features = []
    for f in features_strs:
        f = f.strip()
        if f == '':
            continue
        ff = parse_feature(f)
        features.append(ff)
    return features


def copy_feature(ff):
    return {
        'prop_type': ff['prop_type'],
        'prop_value': ff['prop_value'],
        'value_type': ff['value_type'],
        'calc_order': ff['calc_order']
    }


def merge_features(*args):
    fs = []
    for fl in args:
        if fl is not None:
            for f in fl:
                has_same_feature = False
                for pf in fs:
                    if pf['prop_type'] == f['prop_type'] and pf['value_type'] == f['value_type'] and pf['calc_order'] == f['calc_order']:
                        pf['prop_value'] += f['prop_value']
                        has_same_feature = True
                        break
                if not has_same_feature:
                    fs.append(copy_feature(f))
    return fs


def parse_eot_trigger(eot_trigger_str):
    eot_trigger = eot_trigger_str.split('#')
    tt = {}
    tt['trigger_type'] = eot_trigger[0]
    tt['trigger_prob'] = int(eot_trigger[1])
    tt['trigger_cd'] = int(eot_trigger[2])
    tt['eot_id'] = int(eot_trigger[3])
    tt['param1'] = int(eot_trigger[4])
    return tt


def parse_eot_triggers(eot_triggers_str):
    eot_triggers_strs = eot_triggers_str.split(';')
    eot_triggers = []
    for t in eot_triggers_strs:
        t = t.strip()
        if t == '':
            continue
        tt = parse_eot_trigger(t)
        eot_triggers.append(tt)
    return eot_triggers


def parse_skill_id(skill_id):
    skill_id = int(skill_id)
    skill_level = skill_id % 10000
    skill_type = (skill_id - skill_level) / 10000
    return skill_type, skill_level


def make_skill_id(skill_type, skill_level):
    return int(skill_type * 10000 + skill_level)


def read_skills() -> dict:

    csv_dir = os.environ.get('CSV_DIR')
    skills_csv = os.path.join(csv_dir, 'SkillsTable.csv')

    data = read_csv(skills_csv, 'id')

    for skill_id in data:
        d = data[skill_id]

        # 技能附加属性计算
        if d['features'] != '':
            d['features'] = parse_features(d['features'])
        else:
            d['features'] = []

        if d['projectiles'] != '':
            d['projectiles'] = d['projectiles'].split(';')
        else:
            d['projectiles'] = []

    # 技能的features字段是叠加字段, 之前所有等级的技能的features字段都会叠加到当前技能的features字段中

    skill_ids = list(data.keys())
    # 从小到大排序
    skill_ids.sort(key=lambda x: int(x))
    # print('skill_ids: ', skill_ids)

    for skill_id in skill_ids:
        skill = data[skill_id]
        skill_type, skill_level = parse_skill_id(skill_id)

        if skill_level == 1:
            continue

        if skill_level > 1:
            # 如果当前技能等级大于1, 叠加它前一等级的技能的features字段
            # 因为是从小到大排序的, 所以前一等级的技能一定已经处理过了
            # 所以直接从data中取出前一等级的技能的features字段

            pre_level_skill_id = make_skill_id(skill_type, skill_level - 1)
            pre_level_skill = data[pre_level_skill_id]

            new_features = merge_features(
                skill['features'], pre_level_skill['features'])
            skill['features'] = new_features

    return data


def main():

    data = read_skills()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
