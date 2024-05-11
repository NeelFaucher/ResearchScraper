from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
from dash.dependencies import State
from scrape import scrape_data
import time

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
        # Sample data
        data = {
            'URL': ['http://example.com/page1', 'http://example.com/page2'],
            'Title': ['Sample Title 1', 'Sample Title 2'],
            'Authors': ['Author 1', 'Author 2'],
            'Date': ['2024-05-11', '2024-05-10'],
            'Abstract': ['This is the abstract for page 1.', 'This is the abstract for page 2.']
        }

        # Create DataFrame
        scraped_data = pd.DataFrame(data)

        # Filter DataFrame based on search_value
        if search_value:
            scraped_data = scraped_data[scraped_data['Title'].str.contains(search_value, case=False, regex=False)]

        # Return DataTable
        return dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in scraped_data.columns],
            data=scraped_data.to_dict('records')
        )
    else:
        return ""

# def search_value(n_clicks, search_value):
#     if n_clicks > 0:
#         # Call scrape_data to get the DataFrame
#         scraped_data = scrape_data()  # Assuming scrape_data returns a DataFrame
#         time.sleep(5)
#         if not scraped_data.empty:
#             # Display the DataFrame using Dash DataTable
#             return dash_table.DataTable(
#                 id='data-table',
#                 columns=[{"name": i, "id": i} for i in scraped_data.columns],
#                 data=scraped_data.to_dict('records')
#             )
#         else:
#             return "No data available."
#     else:
#         return ""

if __name__ == '__main__':
    app.run_server(debug=True)