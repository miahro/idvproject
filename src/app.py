"""Module for Dash app."""

import os
from dotenv import load_dotenv

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_manager import normalized_budgets_dict
from data_functions import budget_total_and_balance
from plot import plot_treemap, plot_sunburst, plot_pie, plot_bar, plot_bubble, plot_icicle
# from data_manager import get_or_save_data


normalized_budgets = normalized_budgets_dict()


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
                    {'label': 'Billions of Euros', 'value': 'beuros'}
                ],
                value='percentage'
            ),
        ], style={'width': '25%', 'display': 'inline-block', 'margin-left': '20px'}),
        html.Div([
            html.Label('Budget balance', style={'font-weight': 'bold'}),
            html.P(id='balance'),
        ], style={'width': '10%', 'display': 'inline-block', 'margin-left': '20px'}),
        # html.Div([
        #     html.Label('Budget Year', style={'font-weight': 'bold'}),
        #     dcc.Dropdown(
        #         id='year-dropdown',
        #         options=[{'label': i, 'value': i} for i in range(2014, 2025)],
        #         value=2023
        #     )
        # ], style={'width': '20%', 'display': 'inline-block', 'margin-left': '20px'}),
        html.Div([
            html.Label('Budget Year', style={'font-weight': 'bold'}),
            dcc.Slider(
                id='year-slider',
                min=2014,
                max=2024,
                step=1,
                value=2024,
                marks={i: str(i) for i in range(2014, 2025)},
            )
        ], style={'width': '20%', 'display': 'inline-block', 'margin-left': '20px'}),
        html.Div([
            dcc.RadioItems(
                id='income-expense-radio',
                options=[
                    {'label': 'Income', 'value': 'income'},
                    {'label': 'Expenses', 'value': 'expenses'},
                ],
                value='income'
            ),
        ], style={'width': '10%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'align-items': 'flex-start'}),




    html.Div([
        dcc.Graph(id='graph', style={
                  'display': 'inline-block', 'width': '98%', 'padding-right': '1%'}),
        # dcc.Graph(id='graph2', style={
        #           'display': 'inline-block', 'width': '48%', 'padding-left': '1%'}),
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
                {'label': 'Bubble', 'value': 'bubble'},
                {'label': 'Icicle', 'value': 'icicle'}
            ],
            value='treemap'
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),


])

print(px.colors.sequential)


@ app.callback(
    [Output('graph', 'figure'),
     # Output('graph2', 'figure'),
     Output('balance', 'children'),
     Output('balance', 'style')],
    [Input('year-slider', 'value'),
     Input('normalization-dropdown', 'value'),
     Input('drill-down-dropdown', 'value'),
     Input('graph-type-dropdown', 'value'),
     Input('colorscale-expenses-dropdown', 'value'),
     Input('colorscale-income-dropdown', 'value'),
     Input('income-expense-radio', 'value')]
)
# pylint: disable=R0913, C0301
def update_graph(year, normalization, drilldown, graph_type, colorscale_expenses, colorscale_income, income_expense):
    """Method to update graphs based on user drop down selections"""
    # pylint: disable=R0912, R0915

    df_exp = normalized_budgets[str(year)][f'exp_{normalization}']
    df_inc = normalized_budgets[str(year)][f'inc_{normalization}']

    print(f'chosen year {year}')
    print(f'chosen normalization {normalization}')
    print(f'chonse income-expense {income_expense}')

    _, _, balance = budget_total_and_balance(
        df_inc, df_exp)

    balance_str = f'{balance:.2f}'
    balance_color = {'color': 'green' if balance >=
                     0 else 'red', 'font-weight': 'bold'}

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
    elif graph_type == 'icicle':
        fig1 = plot_icicle(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown)
        fig2 = plot_icicle(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown)
    else:
        raise ValueError("Invalid graph type.")

    fig1.update_layout(
        autosize=False,
        width=1900,
        height=900,
    )

    fig2.update_layout(
        autosize=False,
        width=1900,
        height=900,
    )

    if income_expense == 'income':
        return fig2, balance_str, balance_color
    else:
        return fig1, balance_str, balance_color

    # return fig1, fig2, balance_str, balance_color


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
