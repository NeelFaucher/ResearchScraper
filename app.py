from dash import Dash, html, dcc, Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

data = {
    'A': [1, 2, 3, 4, 5],
    'B': ['a', 'b', 'c', 'd', 'e'],
    'C': [True, False, True, False, True]
}

# Creating the DataFrame
df = pd.DataFrame(data)

app.layout = html.Div([
    html.H1('Joy\'s Scraper'),
    dcc.Input(id='search-bar', type='text', placeholder='Enter value to search...'),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='search-value'),
    html.Div(id='dataframe-output')
])

@app.callback(
    Output('search-value', 'children'),
    [Input('search-button', 'n_clicks')],
    [Input('search-bar', 'value')]
)
def search_value(n_clicks, search_value):
    if n_clicks > 0 and search_value:
        return f'You searched for: {search_value}'
    else:
        return ""

@app.callback(
    Output('dataframe-output', 'children'),
    [Input('search-button', 'n_clicks')],
    [Input('search-bar', 'value')]
)
def display_dataframe(n_clicks, search_value):
    if n_clicks > 0 and search_value:
        result = df[df.eq(search_value).any(1)]
        if not result.empty:
            return result.to_html(index=False)
        else:
            return "No matching rows found."
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)