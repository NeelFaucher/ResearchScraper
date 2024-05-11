from dash import Dash, html, dcc, Input, Output, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
from dash.dependencies import State
from scrape import scrape_data  # Import scrape_data if it's in a separate module

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
def search_value(n_clicks, search_value):
    if n_clicks > 0:
        # Trigger scraping data
        return scrape_data(search_value)
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
        # Data fetched, display DataTable
        return dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in scraped_data.columns],
            data=scraped_data.to_dict('records')
        )

if __name__ == '__main__':
    app.run_server(debug=True)