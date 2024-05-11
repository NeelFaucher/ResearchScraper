from dash import Dash, html, dcc, Input, Output, DataTable, TableColumn
import pandas as pd
from scrape import scrape_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

data = {
    'A': [1, 2, 3, 4, 5],
    'B': ['a', 'b', 'c', 'd', 'e'],
    'C': [True, False, True, False, True]
}
df = pd.DataFrame(data)

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
    [Input('search-bar', 'value')]
)
def search_value(n_clicks, search_value):
    if n_clicks > 0 and search_value:
        # Here you would ideally use search_value to filter data or perform any other operations
        # For now, let's just call scrape_data() and display the DataFrame
        df = scrape_data()
        return DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records')
        )
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)