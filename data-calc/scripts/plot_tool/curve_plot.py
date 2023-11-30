import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox


class CurvePlot:

    # x_to_y_func: callable x: np.array, param: float, y_min: float, y_max: float

    def __init__(self, x_to_y_func: callable, title: str):
        self.x_to_y_func = x_to_y_func
        self.title = title

    def set_x(self, x: np.array, title: str):
        self.x = x
        self.x_title = title

    def set_y(self, y_min: float, y_max: float, title: str):
        self.y_min = y_min
        self.y_max = y_max
        self.y_title = title

    def set_param_range(self, param_min: float, param_max: float, param_step: float = 0.01, param_init: float = 1):
        self.param_min = param_min
        self.param_max = param_max
        self.param_step = param_step
        self.param_init = param_init

    def update(self, event):

        self.y_min_current = float(self.y_min_input.text)
        self.y_max_current = float(self.y_max_input.text)
        self.param_current = float(self.param_slider.val)
        self.param_input.set_val(str(self.param_current))

        self.update_curve()

    def update_input(self, event):

        self.y_min_current = float(self.y_min_input.text)
        self.y_max_current = float(self.y_max_input.text)
        self.param_current = float(self.param_input.text)
        self.param_slider.set_val(self.param_current)

        self.update_curve()

    def update_curve(self):
        self.y = self.x_to_y_func(
            self.x, self.param_current, self.y_min_current, self.y_max_current)
        self.curve.set_ydata(self.y)
        self.ax.set_ylim([self.y_min_current, self.y_max_current])
        self.fig.canvas.draw_idle()

    def set_current_param_callback(self, callback: callable):
        self.current_param_callback = callback

    def on_getdata_clicked(self, event):
        self.y_min_current = float(self.y_min_input.text)
        self.y_max_current = float(self.y_max_input.text)
        y = self.x_to_y_func(self.x, self.param_slider.val,
                             self.y_min_current, self.y_max_current)

        self.current_param_callback({
            'x': self.x.tolist(),
            'y_min': self.y_min_current,
            'y_max': self.y_max_current,
            'param': self.param_slider.val,
            'y': y.tolist()
        })

    def show(self):

        self.fig, self.ax = plt.subplots(num=self.title)
        plt.subplots_adjust(bottom=0.25)

        axes_up_left = plt.axes([0.15, 0.07, 0.3, 0.03])
        axes_up_right = plt.axes([0.6, 0.07, 0.3, 0.03])
        axes_down_left = plt.axes([0.15, 0.02, 0.45, 0.03])
        axes_down_right = plt.axes([0.7, 0.02, 0.2, 0.03])

        self.y_min_input = TextBox(axes_up_left, 'y_min', initial=self.y_min)
        self.y_max_input = TextBox(axes_up_right, 'y_max', initial=self.y_max)
        self.param_slider = Slider(axes_down_left, 'param', valmin=self.param_min,
                                   valmax=self.param_max, valinit=self.param_init, valstep=self.param_step, color='green')
        self.param_input = TextBox(
            axes_down_right, "", initial=self.param_init)

        self.y_min_current = float(self.y_min_input.text)
        self.y_max_current = float(self.y_max_input.text)
        self.param_current = float(self.param_input.text)

        self.y = self.x_to_y_func(
            self.x, self.param_current, self.y_min_current, self.y_max_current)

        self.curve, = self.ax.plot(self.x, self.y, lw=2, color='blue')
        self.ax.set_ylim([self.y_min, self.y_max])

        self.y_min_input.on_submit(self.update)
        self.y_max_input.on_submit(self.update)
        self.param_slider.on_changed(self.update)
        self.param_input.on_submit(self.update_input)

        # Add a getdata button
        getdata_button_ax = plt.axes([0.8, 0.8, 0.1, 0.04])
        getdata_button = plt.Button(
            getdata_button_ax, 'Get Data', color='gray', hovercolor='lightgray')

        getdata_button.on_clicked(self.on_getdata_clicked)

        plt.show()


if __name__ == "__main__":
    # do some test

    print("--------------------")
    print("test curve_plot")
    print("--------------------")

    x = np.linspace(0, 1, 100)
    y_min = 0.0
    y_max = 100
    param_min = 0.0
    param_max = 10.0

    def power_curve_y(x: np.array, param: float, y_min: float, y_max: float):
        return y_min + (y_max - y_min) * x ** param

    p = CurvePlot(power_curve_y, "Curve Plot")
    p.set_x(x, "x")
    p.set_y(y_min, y_max, "y")
    p.set_param_range(param_min, param_max)
    p.set_current_param_callback(lambda data: print(data))
    p.show()
