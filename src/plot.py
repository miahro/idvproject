"""Module for plotly plot functions"""

import plotly.express as px
import pandas as pd


import plotly.graph_objects as go  # pylint: disable=C0412
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
        texttemplate='%{label} <br> Total: %{customdata[0]:.2f}',
        textposition='middle center', textfont_size=12)
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


# def plot_balance_bar(net_income, total_expenses, balance):
#     """
#     Create a Plotly bar plot for the balance.
#     """

#     fig = make_subplots(rows=1, cols=1)

#     fig.add_trace(go.Bar(x=['Net Income', 'Total Expenses', 'Balance'],
#                          y=[net_income, total_expenses, balance],
#                               marker_color='rgb(158,202,225)'))

#     fig.update_layout(title_text='Balance', font_size=10)

#     return fig


def plot_balance_gauge(net_income, total_expenses, balance):
    """
    Create a Plotly gauge chart for the balance.
    """

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=("Total Expenses",
                                        "Balance", "Net Income"),
                        specs=[[{"type": "indicator"},
                                {"type": "indicator"}, {"type": "indicator"}]])

    fig.add_trace(go.Indicator(
        mode="number",
        value=total_expenses,
        number={'font': {'color': 'red'}},
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=balance,
        gauge={
            'axis': {'range': [-total_expenses, max(net_income, total_expenses, balance)]}},
    ), row=1, col=2)
    fig.update_layout(title_text='Balance', font_size=10)

    fig.add_trace(go.Indicator(
        mode="number",
        value=net_income,
        number={'font': {'color': 'green'}},
    ), row=1, col=3)

    return fig


def plot_balance_bar(net_income, total_expenses):
    """
    Create a Plotly bar chart for the balance.
    """

    fig = go.Figure(data=[
        go.Bar(name='Net Income', x=[net_income], y=[
               ''], orientation='h', marker_color='green'),
        go.Bar(name='Total Expenses',
               x=[-total_expenses], y=[''], orientation='h', marker_color='red')
    ])

    fig.update_layout(barmode='relative', title_text='Balance',
                      yaxis_showticklabels=False)

    return fig


def plot_sankey(df, source_column, target_column, value_column):
    """Plot a Sankey diagram from a DataFrame."""

    source = df[source_column]
    target = df[target_column]
    value = df[value_column]

    fig = go.Figure(data=[go.Sankey(
        node={
            'pad': 15,
            'thickness': 20,
            'line': {'color': "black", 'width': 0.5},
            'label': pd.concat([source, target]).unique(),  # List of all nodes
            'color': "blue"
        },
        link={
            'source': [list(pd.concat([source, target]).unique()).index(i)
                       for i in source],  # Indices of source nodes
            'target': [list(pd.concat([source, target]).unique()).index(i)
                       for i in target],  # Indices of target nodes
            'value': value
        }
    )])
    fig.update_layout(title_text="Sankey Diagram", font_size=10)
    return fig
