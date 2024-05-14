"""Module for plotly plot functions"""

import plotly.express as px
from constants import budget_units, color_scales


def plot_treemap(df, path, col_scale, normalization):
    """
    Create a Plotly treemap plot from a DataFrame.
    """

    df = df.copy()

    # path = path[0:drill_down_level]
    color_scale = color_scales[col_scale]

    fig = px.treemap(df, path=path, values='total', custom_data=[
        'total'], color_discrete_sequence=color_scale)

    fig.update_traces(
        textposition='middle center', textfont_size=16)
    fig.update_traces(
        hovertemplate=(
            f'%{{label}} <br> Total: %{{value:.2f}} <br> '
            f'Unit: {budget_units[normalization]}'
        ),
        textfont_size=16
    )

    return fig


def get_summary_data(total_income, net_income, total_expenses, balance):
    """Returns data and style data conditional for the financial summary table."""
    balance_color = 'green' if balance >= 0 else 'red'
    total_income_color = 'green'
    net_income_color = 'green'
    total_expenses_color = 'red'
    data = [{
        'total_income': f'{total_income:.2f}',
        'net_income': f'{net_income:.2f}',
        'total_expenses': f'{total_expenses:.2f}',
        'balance': f'{balance:.2f}',
    }]
    style_data_conditional = [
        {'if': {'column_id': 'total_income'}, 'color': total_income_color},
        {'if': {'column_id': 'net_income'}, 'color': net_income_color},
        {'if': {'column_id': 'total_expenses'}, 'color': total_expenses_color},
        {'if': {'column_id': 'balance'}, 'color': balance_color},
    ]
    return data, style_data_conditional


def get_figure(income_expense, df_inc, df_exp, normalization):
    """Returns a Plotly figure based on selection expenses/income."""
    path_exp = ['Total budget', 'Pääluokan nimi',
                'Menoluvun nimi', 'Menomomentin nimi']
    path_inc = ['Total budget', 'Osaston nimi',
                'Tuloluvun nimi', 'Tulomomentin nimi']
    if income_expense == 'income':
        fig = plot_treemap(df_inc, path_inc, col_scale='greens_r',
                           normalization=normalization)
    elif income_expense == 'expenses':
        fig = plot_treemap(df_exp, path_exp, col_scale='reds_r',
                           normalization=normalization)
    else:
        raise ValueError("Invalid income-expense value")
    fig.update_layout(autosize=False, width=1900, height=850,
                      margin={'t': 25, 'l': 0, 'r': 0, 'b': 0})

    return fig
