import os
import json
import numpy as np

from scripts.plot_tool.curve_plot import CurvePlot

# 使用 power 函数做曲线
# y_min 和 y_max 用于修饰 y 轴的范围
# y_offset 用于修饰曲线 y 轴的底部偏移
# power 用于修饰曲线的弯曲程度


def power_curve_y(x: np.array, power: float, y_min: float, y_max: float):

    # power 函数的曲线是上升速度越来越快, 最后趋近于无穷大，用于已知等级填充数据

    x_min = np.min(x)
    x_max = np.max(x)

    # 0 的 power 次方是 0
    x_offset = -x_min

    # x_max 的 power 次方是 y_max
    # y_max = np.power(x_max + x_offset, power) * y_scale + y_offset
    y_scale = (y_max - y_min) / np.power(x_max + x_offset, power)

    return np.round(np.power((x + x_offset), power) * y_scale + y_min)


if __name__ == "__main__":
    # do some test

    print("--------------------")
    print("test curve_plot_power")
    print("--------------------")

    x = np.linspace(1, 100, 100)
    y_min = 0
    y_max = 100000
    param_min = -10.0
    param_max = 10.0

    p = CurvePlot(power_curve_y, "Curve Plot Power")
    p.set_x(x, "x")
    p.set_y(y_min, y_max, "y")
    p.set_param_range(param_min, param_max)
    p.set_current_param_callback(lambda data: print(data))
    p.show()
