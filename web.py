import os
import dash
from dash import html, dash_table
import pandas as pd

# Create the Dash app instance
app = dash.Dash(__name__)

# Function to update table layout
def serve_layout():
    data = {
    'A': [1, 2, 3, 4, 5],
    'B': ['a', 'b', 'c', 'd', 'e'],
    'C': [True, False, True, False, True]
    }

    # Creating the DataFrame
    df = pd.DataFrame(data)
    
    # Define the layout of your Dash app
    layout = html.Div([
        html.H1("Nature Articles on Enzymatic Degradation of Plastics"),
        # Display the DataFrame as a DataTable
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records')
        )
    ])
    
    return layout

# Set the layout of the Dash app
app.layout = serve_layout

# For Gunicorn to recognize the app
server = app.server

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)