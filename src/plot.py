import plotly.express as px
import pandas as pd


def plot_treemap(df, path, drill_down_level=3):
    """
    Create a Plotly treemap plot from a DataFrame.
    """

    path = path[0:drill_down_level]

    fig = px.treemap(df, path=path, values='total', custom_data=['total'])
    fig.update_traces(
        texttemplate='%{label} <br> Total: %{customdata[0]:.2f}', textposition='middle center', textfont_size=12)
    fig.show()

    level_totals = df.groupby(path[0])['total'].sum()
    df[path[0] + '_total'] = df[path[0]].map(level_totals)
    level_totals = df.groupby([path[0], path[1]])['total'].sum()
    df[path[1] +
        '_total'] = df.set_index([path[0], path[1]]).index.map(level_totals.get)

    level_totals = df.groupby([path[0], path[1], path[2]])['total'].sum()
    df[path[2] + '_total'] = df.set_index([path[0],
                                          path[1], path[2]]).index.map(level_totals.get)
    df[path[0]] = df[path[0]] + ' Total: ' + df[path[0] + '_total'].astype(str)
    df[path[1]] = df[path[1]] + ' Total: ' + df[path[1] + '_total'].astype(str)
    df[path[2]] = df[path[2]] + ' Total: ' + df[path[2] + '_total'].astype(str)

    fig = px.treemap(df, path=path, values='total')
    fig.show()
