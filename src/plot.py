"""Module for plotly plot functions"""

import plotly.express as px


def plot_treemap(df, path, col_scale, drill_down_level=4, title=""):
    """
    Create a Plotly treemap plot from a DataFrame.
    """

    df = df.copy()

    path = path[0:drill_down_level]
    color_scale = getattr(px.colors.sequential, col_scale)

    fig = px.treemap(df, path=path, values='total', custom_data=[
                     'total'], color_discrete_sequence=color_scale)

    fig.update_traces(
        # texttemplate='%{label}: %{customdata[0]:.2f}',
        textposition='middle center', textfont_size=16)
    fig.update_traces(
        hovertemplate='%{label} <br> Total: %{value:.2f}', textfont_size=16)

    fig.update_layout(title_text=title)

    return fig


def plot_sunburst(df, path, col_scale, drill_down_level=4, title=""):
    """
    Create a Plotly sunburst plot from a DataFrame.
    """

    path = path[0:drill_down_level]
    color_scale = getattr(px.colors.sequential, col_scale)

    fig = px.sunburst(df, path=path, values='total',
                      color_discrete_sequence=color_scale)

    fig.update_traces(
        hovertemplate='%{label} <br> Total: %{value:.2f}', textfont_size=12)

    fig.update_layout(title_text=title)
    return fig
