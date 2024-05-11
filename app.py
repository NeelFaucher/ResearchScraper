from dash import Dash, html, dcc, Input, Output, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
from scrape import MyTestClass
from dash.dependencies import State
from seleniumbase import BaseCase

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1("Joy's Scraper"),
    html.Div([
        dcc.Input(id='search-bar', type='text', placeholder='Enter value to search...'),
        html.Button('Search', id='search-button', n_clicks=0),
        html.Div(id='search-output')
    ]),
    html.Div(id='data-table-container')
])

@app.callback(
    Output('search-output', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('search-bar', 'value')]
)
def scrape_data(n_clicks, search_value):
    if n_clicks > 0:
        try:
            test_inst = MyTestClass()
            with test_inst:  # Create an instance and enter its context
                scraped_data = test_inst.test_scrape_data()
            return scraped_data
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={'color': 'red'})
    else:
        raise PreventUpdate

@app.callback(
    Output('data-table-container', 'children'),
    [Input('search-output', 'children')]
)
def display_data_table(scraped_data):
    if scraped_data is None:
        # Data not fetched yet, show loading spinner
        return html.Div("Loading...", style={'textAlign': 'center'})
    else:
        if isinstance(scraped_data, pd.DataFrame):
            return dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in scraped_data.columns],
                data=scraped_data.to_dict('records')
            )
        else:
            return html.Div("No data available", style={'color': 'red'})

if __name__ == '__main__':
    app.run_server(debug=True)