"""Module for Dash app."""

import os
from dotenv import load_dotenv

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_manager import normalized_budgets_dict
from data_functions import budget_total_and_balance, form_title
from plot import plot_treemap, plot_sunburst
# from data_manager import get_or_save_data


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
            html.Label('Budget balance', style={'font-weight': 'bold'}),
            html.P(id='balance'),
        ], style={'width': '10%', 'display': 'inline-block', 'margin-left': '20px'}),
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
                value='beuros'
            ),
        ], style={'width': '22%', 'display': 'inline-block', 'margin-left': '20px'}),

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
            html.Label('Budget type', style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='income-expense-radio',
                options=[
                    {'label': 'Income', 'value': 'income'},
                    {'label': 'Expenses', 'value': 'expenses'},
                ],
                value='income'
            ),
        ], style={'width': '10%', 'display': 'inline-block'}),
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
        html.Label('Graph type'),
        dcc.Dropdown(
            id='graph-type-dropdown',
            options=[
                {'label': 'Treemap', 'value': 'treemap'},
                {'label': 'Sunburst', 'value': 'sunburst'},
            ],
            value='treemap'
        ),
    ], style={'width': '25%', 'display': 'inline-block'}),


])

print(px.colors.sequential)


@ app.callback(
    [Output('graph', 'figure'),
     Output('balance', 'children'),
     Output('balance', 'style')],
    [Input('year-slider', 'value'),
     Input('normalization-dropdown', 'value'),
     Input('drill-down-radioitems', 'value'),
     Input('graph-type-dropdown', 'value'),
     Input('colorscale-expenses-dropdown', 'value'),
     Input('colorscale-income-dropdown', 'value'),
     Input('income-expense-radio', 'value')]
)
# pylint: disable=R0913, C0301, R0914
def update_graph(year, normalization, drilldown, graph_type, colorscale_expenses, colorscale_income, income_expense):
    """Method to update graphs based on user drop down selections"""
    # pylint: disable=R0912, R0915

    df_exp = normalized_budgets[str(year)][f'exp_{normalization}']
    df_inc = normalized_budgets[str(year)][f'inc_{normalization}']

    print(f'chosen year {year}')
    print(f'chosen normalization {normalization}')
    print(f'chonse income-expense {income_expense}')

    total_income, net_income, total_expenses, balance = budget_total_and_balance(
        df_inc, df_exp)

    balance_str = f'{balance:.2f}'
    balance_color = {'color': 'green' if balance >=
                     0 else 'red', 'font-weight': 'bold'}

    path_exp = ['Total budget', 'Pääluokan nimi',
                'Menoluvun nimi', 'Menomomentin nimi']
    path_inc = ['Total budget', 'Osaston nimi',
                'Tuloluvun nimi', 'Tulomomentin nimi']

    title = form_title(year, income_expense, normalization,
                       total_income, net_income, total_expenses)

    if graph_type == 'treemap':
        fig1 = plot_treemap(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown, title=title)
        fig2 = plot_treemap(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown, title=title)
    elif graph_type == 'sunburst':
        fig1 = plot_sunburst(
            df_exp, path_exp, colorscale_expenses, drill_down_level=drilldown, title=title)
        fig2 = plot_sunburst(
            df_inc, path_inc, colorscale_income, drill_down_level=drilldown, title=title)
    else:
        raise ValueError("Invalid graph type.")

    fig1.update_layout(
        autosize=False,
        width=1900,
        height=1000,
    )

    fig2.update_layout(
        autosize=False,
        width=1900,
        height=1000,
    )

    if income_expense == 'income':
        return fig2, balance_str, balance_color
    if income_expense == 'expenses':
        return fig1, balance_str, balance_color
    raise ValueError("Invalid income-expense value")


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
