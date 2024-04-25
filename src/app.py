"""Module for Dash app."""

import os
from dotenv import load_dotenv

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from config import BU23_EXP_URLS, BU23_INC_URLS, BU19_EXP_URLS, \
    BU19_INC_URLS, BU14_EXP_URLS, BU14_INC_URLS
from data_functions import normalize_budget, budget_total_and_balance
from plot import plot_treemap, plot_sunburst, plot_pie, plot_bar, plot_bubble
from data_manager import get_or_save_data


bu23_exp = get_or_save_data(BU23_EXP_URLS, 'data/bu23_exp.csv')
bu23_inc = get_or_save_data(BU23_INC_URLS, 'data/bu23_inc.csv')

bu19_exp = get_or_save_data(BU19_EXP_URLS, 'data/bu19_exp.csv')
bu19_inc = get_or_save_data(BU19_INC_URLS, 'data/bu19_inc.csv')

bu14_exp = get_or_save_data(BU14_EXP_URLS, 'data/bu14_exp.csv')
bu14_inc = get_or_save_data(BU14_INC_URLS, 'data/bu14_inc.csv')


bu23_exp_beuros = normalize_budget(bu23_exp, method='beuros')
bu23_inc_beuros = normalize_budget(bu23_inc, method='beuros')

bu23_exp_percentage = normalize_budget(bu23_exp, method='percentage')
bu23_inc_percentage = normalize_budget(bu23_inc, method='percentage')

bu23_exp_capita = normalize_budget(bu23_exp, method='per_capita')
bu23_inc_capita = normalize_budget(bu23_inc, method='per_capita')

bu23_exp_working_age_capita = normalize_budget(
    bu23_exp, method='per_working_age_capita')
bu23_inc_working_age_capita = normalize_budget(
    bu23_inc, method='per_working_age_capita')

bu23_exp_gdp = normalize_budget(bu23_exp, method='gdp')
bu23_inc_gdp = normalize_budget(bu23_inc, method='gdp')

bu23_exp_big_mac = normalize_budget(bu23_exp, method='big_mac')
bu23_inc_big_mac = normalize_budget(bu23_inc, method='big_mac')

bu23_exp_milk = normalize_budget(bu23_exp, method='milk_cartons')
bu23_inc_milk = normalize_budget(bu23_inc, method='milk_cartons')

bu23_exp_pizzas = normalize_budget(bu23_exp, method='pizzas')
bu23_inc_pizzas = normalize_budget(bu23_inc, method='pizzas')

bu23_exp_median_monthly_salary = normalize_budget(
    bu23_exp, method='median_monthly_salary')
bu23_inc_median_monthly_salary = normalize_budget(
    bu23_inc, method='median_monthly_salary')


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Budget visualization", style={
                'textAlign': 'left', 'display': 'inline-block'}),

        html.Div([
            html.Label('Normalization / budget unit',
                       style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='normalization-dropdown',
                options=[
                    {'label': 'Per cent from total budget', 'value': 'percentage'},
                    {'label': 'Per Capita', 'value': 'per_capita'},
                    {'label': 'Per Working Age Capita',
                        'value': 'per_working_age_capita'},
                    {'label': 'Per cent of GDP', 'value': 'gdp'},
                    {'label': 'Big Macs per capita', 'value': 'big_mac'},
                    {'label': 'Milk Cartons per capita', 'value': 'milk_cartons'},
                    {'label': 'Pizzas per capita', 'value': 'pizzas'},
                    {'label': 'Median Monthly Salaries per working age capita',
                        'value': 'median_monthly_salary'},
                    {'label': 'Billions of Euros', 'value': 'Beuros'}
                ],
                value='percentage'
            ),
        ], style={'width': '25%', 'display': 'inline-block', 'margin-left': '20px'}),
        html.Div([
            html.Label('Budget balance', style={'font-weight': 'bold'}),
            html.P(id='balance'),
        ], style={'width': '20%', 'display': 'inline-block', 'margin-left': '20px'}),

    ], style={'display': 'flex', 'align-items': 'flex-start'}),

    html.Div([
        dcc.Graph(id='graph1', style={
                  'display': 'inline-block', 'width': '48%', 'padding-right': '1%'}),
        dcc.Graph(id='graph2', style={
                  'display': 'inline-block', 'width': '48%', 'padding-left': '1%'}),
    ]),

    html.Div("Below dropdown menus for development purposes only, removed from final app", style={
             'textAlign': 'center'}),

    html.Div([
        html.Label('Color Scale for Expenses'),
        dcc.Dropdown(
            id='colorscale-expenses-dropdown',
            options=[{'label': i, 'value': i}
                     for i in dir(px.colors.sequential)],
            value='Reds_r'
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Color Scale for Income'),
        dcc.Dropdown(
            id='colorscale-income-dropdown',
            options=[{'label': i, 'value': i}
                     for i in dir(px.colors.sequential)],
            value='Greens_r'
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Drill-down level'),
        dcc.Dropdown(
            id='drill-down-dropdown',
            options=[
                {'label': '1', 'value': 1},
                {'label': '2', 'value': 2},
                {'label': '3', 'value': 3},
            ],
            value=2
        ),
    ], style={'width': '15%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Graph type'),
        dcc.Dropdown(
            id='graph-type-dropdown',
            options=[
                {'label': 'Treemap', 'value': 'treemap'},
                {'label': 'Sunburst', 'value': 'sunburst'},
                {'label': 'Pie', 'value': 'pie'},
                {'label': 'Bar', 'value': 'bar'},
                {'label': 'Bubble', 'value': 'bubble'}
            ],
            value='treemap'
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),


])

print(px.colors.sequential)


@ app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('balance', 'children'),
     Output('balance', 'style')],
    [Input('normalization-dropdown', 'value'),
     Input('drill-down-dropdown', 'value'),
     Input('graph-type-dropdown', 'value'),
     Input('colorscale-expenses-dropdown', 'value'),
     Input('colorscale-income-dropdown', 'value')]
)
def update_graph(normalization, drilldown, graph_type, colorscale_expenses, colorscale_income):
    """Method to update graphs based on user drop down selections"""
    # pylint: disable=R0912
    if normalization == 'percentage':
        df_exp = bu23_exp_percentage
        df_inc = bu23_inc_percentage
    elif normalization == 'per_capita':
        df_exp = bu23_exp_capita
        df_inc = bu23_inc_capita
    elif normalization == 'per_working_age_capita':
        df_exp = bu23_exp_working_age_capita
        df_inc = bu23_inc_working_age_capita
    elif normalization == 'gdp':
        df_exp = bu23_exp_gdp
        df_inc = bu23_inc_gdp
    elif normalization == 'big_mac':
        df_exp = bu23_exp_big_mac
        df_inc = bu23_inc_big_mac
    elif normalization == 'milk_cartons':
        df_exp = bu23_exp_milk
        df_inc = bu23_inc_milk
    elif normalization == 'pizzas':
        df_exp = bu23_exp_pizzas
        df_inc = bu23_inc_pizzas
    elif normalization == 'median_monthly_salary':
        df_exp = bu23_exp_median_monthly_salary
        df_inc = bu23_inc_median_monthly_salary
    elif normalization == 'Beuros':
        df_exp = bu23_exp_beuros
        df_inc = bu23_inc_beuros
    else:
        raise ValueError("Invalid normalization method.")

    print(f'chosen normalization {normalization}')

    path_exp = ['Pääluokan nimi', 'Menoluvun nimi', 'Menomomentin nimi']
    path_inc = ['Osaston nimi', 'Tuloluvun nimi', 'Tulomomentin nimi']

    if graph_type == 'treemap':
        fig1 = plot_treemap(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown)
        fig2 = plot_treemap(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown)
    elif graph_type == 'sunburst':
        fig1 = plot_sunburst(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown)
        fig2 = plot_sunburst(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown)
    elif graph_type == 'pie':
        fig1 = plot_pie(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown)
        fig2 = plot_pie(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown)
    elif graph_type == 'bar':
        fig1 = plot_bar(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown)
        fig2 = plot_bar(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown)
    elif graph_type == 'bubble':
        fig1 = plot_bubble(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown)
        fig2 = plot_bubble(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown)
    else:
        raise ValueError("Invalid graph type.")

    fig1.update_layout(
        autosize=False,
        width=1100,
        height=1000,
    )

    fig2.update_layout(
        autosize=False,
        width=1100,
        height=1000,
    )

    _, _, balance = budget_total_and_balance(
        df_inc, df_exp)

    balance_str = f'{balance:.2f}'
    balance_color = {'color': 'green' if balance >=
                     0 else 'red', 'font-weight': 'bold'}

    return fig1, fig2, balance_str, balance_color


if __name__ == '__main__':
    load_dotenv()
    dep_env = os.getenv('PRODUCTION', 'True') == 'True'
    print(f'deployment environment: {dep_env}')
    if dep_env:
        print('running in production mode')
        app.run_server(host='0.0.0.0', port=8050)
    else:
        print('running in development mode')
        app.run_server(debug=True)
