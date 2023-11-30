#!/usr/bin/env python3
# -*- coding: utf8 -*-


# 游戏进度区间内  玩家等级下限为 1
PLAYER_RANK_MIN = 1

# 游戏进度区间内 玩家等级上限为 60
PLAYER_RANK_MAX = 60

# 游戏进度区间内 关卡个数为 20
DUNGEON_LEVEL_COUNT = 20

# 游戏进度区间内 玩家属性获取量为 300
PLAYER_PROP_COUNT = 300

# 从属性投放计算出金币投放后 为了防止玩家过弱导致无法通关的情况 会对金币投放进行强化
COIN_DELIVER_REDUNDANCY = 1.1

# 生成投射物数恒定为1的技能列表
PROJ_COUNT_1_SKILLS = ['Skill4']

# 操作难度影响技能评分的权重
OPERATION_DIFFICULTY_WEIGHT_EASY = 1.5
OPERATION_DIFFICULTY_WEIGHT_HARD = 0.5
