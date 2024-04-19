import plotly.express as px
import pandas as pd


import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_treemap(df, path, col_scale, drill_down_level=3):
    """
    Create a Plotly treemap plot from a DataFrame.
    """

    path = path[0:drill_down_level]
    color_scale = getattr(px.colors.sequential, col_scale)

    fig = px.treemap(df, path=path, values='total', custom_data=[
                     'total'], color_discrete_sequence=color_scale)
    fig.update_traces(
        texttemplate='%{label} <br> Total: %{customdata[0]:.2f}', textposition='middle center', textfont_size=12)
    fig.update_traces(
        hovertemplate='%{label} <br> Total: %{value:.2f}', textfont_size=12)

    return fig


def plot_sunburst(df, path, col_scale, drill_down_level=3):
    """
    Create a Plotly sunburst plot from a DataFrame.
    """

    # df = df_in.copy()

    path = path[0:drill_down_level]
    color_scale = getattr(px.colors.sequential, col_scale)

    # fig = px.sunburst(df, path=path, values='total',
    #                   color_discrete_sequence=color_scale)
    # df[path[-1]] = df[path[-1]] + '<br>Total: ' + df['total'].astype(str)

    fig = px.sunburst(df, path=path, values='total',
                      color_discrete_sequence=color_scale)

    fig.update_traces(
        hovertemplate='%{label} <br> Total: %{value:.2f}', textfont_size=12)
    return fig


def plot_sankey(df, source_column, target_column, value_column):
    # Prepare data
    source = df[source_column]
    target = df[target_column]
    value = df[value_column]

    # Create a Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=pd.concat([source, target]).unique(),  # List of all nodes
            color="blue"
        ),
        link=dict(
            source=[list(pd.concat([source, target]).unique()).index(i)
                    for i in source],  # Indices of source nodes
            target=[list(pd.concat([source, target]).unique()).index(i)
                    for i in target],  # Indices of target nodes
            value=value
        )
    )])

    fig.update_layout(title_text="Sankey Diagram", font_size=10)
    return fig
