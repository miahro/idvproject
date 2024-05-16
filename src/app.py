"""Module for Dash app."""

import os
from dotenv import load_dotenv

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from data_manager import normalized_budgets_dict
from data_functions import budget_total_and_balance
from plot import get_figure, get_summary_data
from constants import budget_units
from help import get_modal_content

normalized_budgets = normalized_budgets_dict()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Finnish State Budget'

help_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Help/Info")),
        dbc.ModalBody(get_modal_content()),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-help",
                       className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal-help",
    is_open=False,
    size='xl'
)

trigger_button = html.Button('Help/Info', id='open-help', n_clicks=0)


app.layout = html.Div([
    html.Div([
        html.Div([
            html.P("State budget", style={
                   'margin-top': '0', 'margin-bottom': '5px', 'font-weight': 'bold'}),
            html.Img(src="https://flagcdn.com/w320/fi.png",
                     height="33px", width="54px", style={'margin-left': '30px',
                                                         'vertical-align': 'top'}),
        ], style={'width': '8%', 'display': 'inline-block',
                  'vertical-align': 'top', 'margin-left': '20px'}),
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
        ], style={'width': '22%', 'display': 'inline-block',
                  'margin-left': '20px', 'margin-top': '5px'}),

        html.Div([
            html.Label('Budget unit (normalization)',
                       style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='normalization-dropdown',
                options=[{'label': value, 'value': key}
                         for key, value in budget_units.items()],
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
            ], style={'margin-top': '6px'})
        ], style={'width': '25%', 'display': 'inline-block', 'margin-left': '20px'}),


        html.Div([
            html.Label('View', style={
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
        html.Div([trigger_button, help_modal]),
    ], style={'display': 'flex', 'align-items': 'flex-start', 'backgroundColor': 'lightgrey'}),

    html.Div([
        dcc.Graph(id='graph', style={
                  'display': 'inline-block', 'width': '98%', 'padding-right': '1%'}),
    ]),

])


def get_financial_data(year, normalization):
    """Returns income and expense dataframes for a given year and normalization."""
    df_inc = normalized_budgets[str(year)][f'inc_{normalization}']
    df_exp = normalized_budgets[str(year)][f'exp_{normalization}']
    total_income, net_income, total_expenses, balance = budget_total_and_balance(
        df_inc, df_exp)
    return df_inc, df_exp, total_income, net_income, total_expenses, balance


@app.callback(
    [Output('graph', 'figure'),
     Output('financial-summary', 'data'),
     Output('financial-summary', 'style_data_conditional')],
    [Input('year-slider', 'value'),
     Input('normalization-dropdown', 'value'),
     Input('income-expense-radio', 'value')]
)
def update_graph(year, normalization, income_expense):
    """Updates the graph based on user input."""
    df_inc, df_exp, total_income, net_income, total_expenses, balance = get_financial_data(
        year, normalization)
    fig = get_figure(income_expense, df_inc, df_exp, normalization)
    data, style_data_conditional = get_summary_data(
        total_income, net_income, total_expenses, balance)
    return fig, data, style_data_conditional


@app.callback(
    Output("modal-help", "is_open"),
    [Input("open-help", "n_clicks"), Input("close-help", "n_clicks")],
    [dash.dependencies.State("modal-help", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """Toggles the modal."""
    if n1 or n2:
        return not is_open
    return is_open


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
