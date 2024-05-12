"""Module for Dash app."""

import os
from dotenv import load_dotenv

import dash
import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output
from data_manager import normalized_budgets_dict
from data_functions import budget_total_and_balance
from plot import plot_treemap

normalized_budgets = normalized_budgets_dict()

app = dash.Dash(__name__)
app.title = 'Finnish State Budget'

app.layout = html.Div([
    html.Div([
        html.Div([
            # Remove top margin
            html.P("State budget", style={
                   'margin-top': '0', 'font-weight': 'bold'}),
            html.Img(src="https://flagcdn.com/w320/fi.png",
                     height="33px", width="54px"),
        ], style={'width': '8%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            dash_table.DataTable(
                id='financial-summary',
                columns=[
                    {"name": "Income", "id": "total_income"},
                    {"name": "Net Income", "id": "net_income"},
                    {"name": "Expenses", "id": "total_expenses"},
                    {"name": "Balance", "id": "balance"},
                ],
                data=[{}],
                style_cell={'textAlign': 'left'},
            )
        ], style={'width': '22%', 'display': 'inline-block', 'margin-left': '20px'}),

        html.Div([
            html.Label('Normalization / budget unit',
                       style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='normalization-dropdown',
                options=[
                    {'label': 'Billions of Euros', 'value': 'beuros'},
                    {'label': 'Per cent from total budget', 'value': 'percentage'},
                    {'label': 'Per cent of GDP', 'value': 'gdp'},
                    {'label': 'Euros per Capita', 'value': 'per_capita'},
                    {'label': 'Euros per Working Age Capita',
                        'value': 'per_working_age_capita'},
                    {'label': 'Big Macs per capita', 'value': 'big_mac'},
                    {'label': 'Milk Cartons per capita', 'value': 'milk_cartons'},
                    {'label': 'Pizzas per capita', 'value': 'pizzas'},
                    {'label': 'Median Monthly Salaries per working age capita',
                        'value': 'median_monthly_salary'}
                ],
                value='beuros',
                clearable=False,
                style={'margin-top': '6px'}
            ),
        ], style={'width': '25%', 'display': 'inline-block', 'margin-left': '20px'}),
        html.Div([
            html.Label('Budget Year', style={'font-weight': 'bold'}),
            html.Div([
                dcc.Slider(
                    id='year-slider',
                    min=2014,
                    max=2024,
                    step=1,
                    value=2024,
                    marks={i: str(i) for i in range(2014, 2025)},
                )
            ], style={'margin-top': '10px'})
        ], style={'width': '25%', 'display': 'inline-block', 'margin-left': '20px'}),


        html.Div([
            html.Label('Display', style={
                       'font-weight': 'bold'}),
            dcc.RadioItems(
                id='income-expense-radio',
                options=[
                    {'label': 'Income', 'value': 'income'},
                    {'label': 'Expenses', 'value': 'expenses'},
                ],
                value='income'
            ),
        ], style={'width': '10%', 'display': 'inline-block', 'margin-left': '20px'}),
        html.Div([
            html.Label('Details', style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='drill-down-radioitems',
                options=[
                    {'label': 'Detailed', 'value': 4},
                    {'label': 'Medium', 'value': 3},
                    {'label': 'Low', 'value': 2},
                ],
                value=4
            ),
        ], style={'width': '15%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'align-items': 'flex-start'}),




    html.Div([
        dcc.Graph(id='graph', style={
                  'display': 'inline-block', 'width': '98%', 'padding-right': '1%'}),
    ]),

])
# pylint: disable=R0914


@ app.callback(
    [Output('graph', 'figure'),
     Output('financial-summary', 'data'),
     Output('financial-summary', 'style_data_conditional')],
    [Input('year-slider', 'value'),
     Input('normalization-dropdown', 'value'),
     Input('drill-down-radioitems', 'value'),
     Input('income-expense-radio', 'value')]
)
def update_graph(year, normalization, drilldown, income_expense):
    """Method to update graphs based on user drop down selections"""

    df_exp = normalized_budgets[str(year)][f'exp_{normalization}']
    df_inc = normalized_budgets[str(year)][f'inc_{normalization}']

    print(f'chosen year {year}')
    print(f'chosen normalization {normalization}')
    print(f'chosen income-expense {income_expense}')

    total_income, net_income, total_expenses, balance = budget_total_and_balance(
        df_inc, df_exp)

    balance_color = 'green' if balance >= 0 else 'red'
    total_income_color = 'green'
    net_income_color = 'green'
    total_expenses_color = 'red'

    path_exp = ['Total budget', 'Pääluokan nimi',
                'Menoluvun nimi', 'Menomomentin nimi']
    path_inc = ['Total budget', 'Osaston nimi',
                'Tuloluvun nimi', 'Tulomomentin nimi']

    # title = form_title(year, income_expense, normalization,
    #                    total_income, net_income, total_expenses)

    if income_expense == 'income':
        fig = plot_treemap(
            df_inc, path_inc, col_scale='greens_r', drill_down_level=drilldown)
    elif income_expense == 'expenses':
        fig = plot_treemap(
            df_exp, path_exp, col_scale='reds_r', drill_down_level=drilldown)
    else:
        raise ValueError("Invalid income-expense value")

    fig.update_layout(
        autosize=False,
        width=1900,
        height=850,
        margin={'t': 25, 'l': 0, 'r': 0, 'b': 0},
    )

    data = [{
        'total_income': f'{total_income:.2f}',
        'net_income': f'{net_income:.2f}',
        'total_expenses': f'{total_expenses:.2f}',
        'balance': f'{balance:.2f}',
    }]

    style_data_conditional = [
        {
            'if': {'column_id': 'total_income'},
            'color': total_income_color,
        },
        {
            'if': {'column_id': 'net_income'},
            'color': net_income_color,
        },
        {
            'if': {'column_id': 'total_expenses'},
            'color': total_expenses_color,
        },
        {
            'if': {'column_id': 'balance'},
            'color': balance_color,
        },
    ]
    return fig, data, style_data_conditional


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
