from dash import Dash, html, dcc, Input, Output
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

data = {
    'URL': urls[:2],
    'Title': titles,
    'Authors': authors_list,
    'Date': dates,
    'Abstract': abstracts
}

# Create a DataFrame
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
        filtered_df = df[df['Title'].str.contains(search_value, case=False, regex=False)]
        return dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in filtered_df.columns],
            data=filtered_df.to_dict('records')
        )
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)