import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from config import BU23_EXP_URLS, BU23_INC_URLS
from data_functions import build_budget
from plot import plot_treemap

# Assuming these are your dataframes
df1 = build_budget(BU23_EXP_URLS)
df2 = build_budget(BU23_INC_URLS)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Main Title", style={'textAlign': 'center'}),
    html.Div("Some text", style={'textAlign': 'center'}),

    # html.Img(src='/assets/image.jpg'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'DataFrame 1', 'value': 'df1'},
            {'label': 'DataFrame 2', 'value': 'df2'}
        ],
        value='df1'
    ),
    # html.Div([
    #     dcc.Graph(id='graph1', style={
    #               'width': '100%'}),
    #     dcc.Graph(id='graph2', style={
    #               'width': '100%'}),
    # ])

    html.Div([
        dcc.Graph(id='graph1', style={
                  'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='graph2', style={
                  'display': 'inline-block', 'width': '49%'}),
    ])
])


@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure')],
    [Input('dropdown', 'value')]
)
def update_graph(value):
    if value == 'df1':
        df = df1
        path = ['Pääluokan nimi', 'Menoluvun nimi', 'Menomomentin nimi']
    else:
        df = df2
        path = ['Osaston nimi', 'Tuloluvun nimi', 'Tulomomentin nimi']

    fig1 = plot_treemap(df, path, drill_down_level=2)
    fig1.update_layout(
        autosize=False,
        width=1100,
        height=1000,
    )
    fig2 = plot_treemap(df, path, drill_down_level=2)
    fig2.update_layout(
        autosize=False,
        width=1100,
        height=1000,
    )

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
