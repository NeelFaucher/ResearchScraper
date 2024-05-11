from dash import Dash, html, dcc, Input, Output
import pandas as pd
from scrape import scrape_data  # Import the scrape_data function

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1("Joy's Scraper"),
    html.Button('Scrape Data', id='scrape-button', n_clicks=0),
    html.Div(id='data-display')
])

@app.callback(
    Output('data-display', 'children'),
    [Input('scrape-button', 'n_clicks')]
)
def display_data(n_clicks):
    if n_clicks > 0:
        df = scrape_data()  # Call the scrape_data function
        # Convert DataFrame to HTML table
        table = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody([html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))])
        ])
        return table
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)