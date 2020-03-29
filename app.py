import dash
from datetime import datetime
import pandas as pd
import requests
import os

from dotenv import load_dotenv

import  dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas_datareader.data as web
import secrets

##### add env variables
if os.path.isfile(".env"):
    load_dotenv()
    print("Loading environment variables...")
else:
    pass

########### Define your variables
tabtitle='Bull Market'


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
my_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = my_app.server
my_app.title=tabtitle

######### Initial Layout
my_app.layout = html.Div([
    html.H1('Hello Bulls'),
    html.Span('Stock Ticker:'),
    html.Br(),
    dcc.Input(
            value = 'TSLA',
            id = 'my-input'
        ),
    dcc.Graph(id = 'my-graph')
    ])

###### Update chart dynamically
@my_app.callback(
    Output('my-graph','figure'),
    [Input('my-input','value')]
)
def update_graph(stock_ticker):
    fun = "TIME_SERIES_DAILY_ADJUSTED"
    url  = "https://www.alphavantage.co/query?function=" + fun + "&symbol=" + stock_ticker + "&outputsize=full&apikey=" + os.getenv('ALPHA_VANTAGE_KEY')
    df = pd.DataFrame.from_dict(requests.get(url).json().get('Time Series (Daily)',None),orient = 'index')
    df.columns = df.columns.str.split(".").str[1].str.strip().str.lower().str.replace(' ', '_')
    figure = {
        'data': [
            {
                'x': df.index,
                'y': df.close
            }
        ]
    }
    return figure

if __name__ == '__main__':
    my_app.run_server()