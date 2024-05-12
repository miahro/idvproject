"""utility for interpolating colors from a color scale"""

import numpy as np
import plotly.express as px


def interpolate_colors(color_list, num_colors):
    """Interpolate colors from a color scale"""
    colors = np.array(
        [[int(c) for c in color.strip('rgb()').split(',')] for color in color_list])

    new_indices = np.linspace(0, len(color_list) - 1, num_colors)

    new_colors = []

    for i in new_indices:
        lower_index = int(np.floor(i))
        upper_index = int(np.ceil(i))
        fraction = i - lower_index

        new_color = (1 - fraction) * \
            colors[lower_index] + fraction * colors[upper_index]

        new_color = tuple(np.round(new_color).astype(int))

        new_colors.append('rgb' + str(new_color))

    return new_colors


if __name__ == '__main__':

    reds_r = ['rgb(0,68,27)', 'rgb(0,109,44)', 'rgb(35,139,69)', 'rgb(65,171,93)',
              'rgb(116,196,118)', 'rgb(161,217,155)', 'rgb(199,233,192)',
              'rgb(229,245,224)', 'rgb(247,252,245)']

    extended_reds_r = interpolate_colors(
        getattr(px.colors.sequential, 'Reds_r'), 15)

    print(extended_reds_r)
