import dash
from dash import html, dcc, Input, Output, State
from bs import scrape_bs

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Joy's Scraper"),
    dcc.Input(id='search-bar', type='text', placeholder='Enter value to search...'),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='search-output')
])

@app.callback(
    Output('search-output', 'children'),
    [Input('search-button', 'n_clicks')],
    [State('search-bar', 'value')]
)
def scrape_data(n_clicks, search_value):
    if n_clicks > 0:
        # Call the scrape function and return its result
        scraped_data = scrape_bs(search_value)
        return html.Div(scraped_data)
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)