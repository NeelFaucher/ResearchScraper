import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from tasks import scrape_2

app = dash.Dash(__name__)
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

def scrape():
    # Your scraping logic goes here
    # For demonstration, let's assume scraped_data is a string
    scraped_data = scrape_2.delay()
    return scraped_data

@app.callback(
    Output('search-output', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('search-bar', 'value')]
)
def scrape_data(n_clicks, search_value):
    if n_clicks > 0:
        # Call the scrape function and return its result
        scraped_data = scrape()
        return html.Div(scraped_data)
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
        return html.Div(scraped_data, style={'color': 'blue'})

if __name__ == '__main__':
    app.run_server(debug=True)