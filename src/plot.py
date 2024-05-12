"""Module for plotly plot functions"""

import plotly.express as px

color_scales = {
    'reds_r': ['rgb(103, 0, 13)', 'rgb(138, 9, 18)', 'rgb(170, 16, 22)',
               'rgb(192, 21, 27)', 'rgb(213, 34, 33)', 'rgb(234, 54, 42)',
               'rgb(244, 79, 57)', 'rgb(251, 106, 74)', 'rgb(252, 129, 97)',
               'rgb(252, 152, 121)', 'rgb(252, 175, 148)', 'rgb(253, 198, 175)',
               'rgb(254, 219, 203)', 'rgb(254, 233, 223)', 'rgb(255, 245, 240)'],
    'greens_r': ['rgb(0,68,27)', 'rgb(0,109,44)', 'rgb(35,139,69)', 'rgb(65,171,93)',
                 'rgb(116,196,118)', 'rgb(161,217,155)', 'rgb(199,233,192)',
                 'rgb(229,245,224)', 'rgb(247,252,245)']
}


def plot_treemap(df, path, col_scale, drill_down_level=4, title=""):
    """
    Create a Plotly treemap plot from a DataFrame.
    """

    df = df.copy()

    path = path[0:drill_down_level]
    color_scale = color_scales[col_scale]

    fig = px.treemap(df, path=path, values='total', custom_data=[
        'total'], color_discrete_sequence=color_scale)

    fig.update_traces(
        # texttemplate='%{label}: %{customdata[0]:.2f}',
        textposition='middle center', textfont_size=16)
    fig.update_traces(
        hovertemplate='%{label} <br> Total: %{value:.2f}', textfont_size=16)

    fig.update_layout(title_text=title)

    return fig
