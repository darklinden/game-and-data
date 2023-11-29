import os
import json
import numpy as np

from scripts.plot_tool.curve_plot import CurvePlot

# 使用 tanh 函数做曲线
# y_min 和 y_max 用于修饰 y 轴的范围
# y_offset 用于修饰曲线 y 轴的底部偏移
# param 用于修饰曲线的弯曲程度


def tanh_curve_y(x: np.array, param: float, y_min: float, y_max: float):

    # tanh 函数的曲线是上升速度越来越慢, 最后趋近于 1, 用于已知上限拆分数据

    x_min = np.min(x)
    x_max = np.max(x)

    # 0 的 tanh 是 0
    x_offset = -x_min

    # x_max 的 tanh 是 y_max
    # y_max = np.tanh(x_max + x_offset, param) * y_scale + y_min
    y_scale = (y_max - y_min) / np.tanh((x_max + x_offset) * param)

    return np.round(np.tanh((x + x_offset) * param) * y_scale + y_min)


if __name__ == "__main__":
    # do some test

    print("--------------------")
    print("test curve_plot_tanh")
    print("--------------------")

    x = np.linspace(1, 100, 100)
    y_min = 0
    y_max = 100000
    param_min = -0.2
    param_max = 0.6
    param_step = 0.0001

    p = CurvePlot(tanh_curve_y, "Curve Plot Tanh")
    p.set_x(x, "x")
    p.set_y(y_min, y_max, "y")
    p.set_param_range(param_min, param_max, param_step)
    p.set_current_param_callback(lambda data: print(data))
    p.show()
