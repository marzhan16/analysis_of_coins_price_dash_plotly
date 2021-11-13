# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc
import plotly      
import plotly.express as px
import pandas as pd    

import requests
from datetime import datetime

import plotly.graph_objects as go



#--------------------------------------------Data-----------------------------------

data_requests = requests.get(
        "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"
    )
json_data = data_requests.json()
df = pd.DataFrame(json_data)

df[['date','prices']] = pd.DataFrame(df.prices.tolist(), index= df.index)
df[['date1','market_caps']] = pd.DataFrame(df.market_caps.tolist(), index= df.index)
df[['date2','total_volumes']] = pd.DataFrame(df.total_volumes.tolist(), index= df.index)
df = df[['date', 'prices', 'market_caps', 'total_volumes', 'date1', 'date2']]
df['date'] = df['date']//1000

df.drop(columns=['date1', 'date2'], inplace = True)


date = []
df['date'].to_list()
for i in df.date:
    ts = int(i)
    date.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    
df['date'] = date

another_dataframe = df[["date","prices", "market_caps", 'total_volumes']]
new_df = another_dataframe.copy()


df['date'] = [i[:10] for i in df['date']]


df['day'] = pd.DatetimeIndex(df['date']).day_name()

start_date = df['date'][0]
end_date = df['date'].to_list()[-1]


#-----------------------------------------------Cards---------------------------------------


min_price = df['prices'].min()
date_of_min_price = df.loc[df['prices'] == df['prices'].min(),'date'].to_string(index=False)

max_price = df['prices'].max()
date_of_max_price = df.loc[df['prices'] == df['prices'].max(),'date'].to_string(index=False)

max_total_volume = df['total_volumes'].max()
date_of_max_total_volume = df.loc[df['total_volumes'] == df['total_volumes'].max(),'date'].to_string(index=False)

min_total_volume = df['total_volumes'].min()
date_of_min_total_volume = df.loc[df['total_volumes'] == df['total_volumes'].min(),'date'].to_string(index=False)

max_market_caps = df['market_caps'].max()
date_of_max_market_caps = df.loc[df['market_caps'] == df['market_caps'].max(),'date'].to_string(index=False)

min_market_caps = df['market_caps'].min()
date_of_min_market_caps = df.loc[df['market_caps'] == df['market_caps'].min(),'date'].to_string(index=False)


#-----------------------------------------------Mean dataframe------------------------------

days = [x for x in df['day'].unique()]
mean_prices = df.groupby(['day'])['prices'].mean().loc[days]
mean_total_volumes = df.groupby(['day'])['total_volumes'].mean().loc[days]
mean_market_caps = df.groupby(['day'])['market_caps'].mean().loc[days]

df_mean = {
    'days': [x for x in days], 
    'mean_prices': [x for x in mean_prices], 
    'mean_total_volumes':[x for x in mean_total_volumes],
    'mean_market_caps':[x for x in mean_market_caps]
}


df_mean = pd.DataFrame(df_mean)


#---------------------------------------------------------------------------------


#---------------------------------Ethereum data-------------------------------


data_requests_ethereum = requests.get(
        "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=30"
    )
json_data_ethereum = data_requests_ethereum.json()
df_ethereum = pd.DataFrame(json_data_ethereum)

df_ethereum[['date','prices']] = pd.DataFrame(df_ethereum.prices.tolist(), index= df_ethereum.index)
df_ethereum[['date1','market_caps']] = pd.DataFrame(df_ethereum.market_caps.tolist(), index= df_ethereum.index)
df_ethereum[['date2','total_volumes']] = pd.DataFrame(df_ethereum.total_volumes.tolist(), index= df_ethereum.index)
df_ethereum = df_ethereum[['date', 'prices', 'market_caps', 'total_volumes', 'date1', 'date2']]
df_ethereum['date'] = df_ethereum['date']//1000

df_ethereum.drop(columns=['date1', 'date2'], inplace = True)


date = []
df_ethereum['date'].to_list()
for i in df_ethereum.date:
    ts = int(i)
    date.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    
df_ethereum['date'] = date

another_dataframe_ethereum = df_ethereum[["date","prices", "market_caps", 'total_volumes']]
new_df_ethereum = another_dataframe_ethereum.copy()


df_ethereum['date'] = [i[:10] for i in df_ethereum['date']]


df_ethereum['day'] = pd.DatetimeIndex(df_ethereum['date']).day_name()

df_one_day_ethereum = df_ethereum.groupby(df_ethereum['date']).sum().reset_index()

start_date_ethereum = new_df_ethereum['date'][0]
end_date_ethereum = new_df_ethereum['date'].to_list()[-1]


#---------------------------------------------------------------------------------

#-----------------------------------------Bitcoin Data-----------------------------------

data_requests_cardano = requests.get(
        "https://api.coingecko.com/api/v3/coins/cardano/market_chart?vs_currency=usd&days=30"
    )
json_data_cardano = data_requests_cardano.json()
df_cardano = pd.DataFrame(json_data_cardano)

df_cardano[['date','prices']] = pd.DataFrame(df_cardano.prices.tolist(), index= df_cardano.index)
df_cardano[['date1','market_caps']] = pd.DataFrame(df_cardano.market_caps.tolist(), index= df_cardano.index)
df_cardano[['date2','total_volumes']] = pd.DataFrame(df_cardano.total_volumes.tolist(), index= df_cardano.index)
df_cardano = df_cardano[['date', 'prices', 'market_caps', 'total_volumes', 'date1', 'date2']]
df_cardano['date'] = df_cardano['date']//1000

df_cardano.drop(columns=['date1', 'date2'], inplace = True)


date = []
df_cardano['date'].to_list()
for i in df_cardano.date:
    ts = int(i)
    date.append(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    
df_cardano['date'] = date

another_dataframe_cardano = df_cardano[["date","prices", "market_caps", 'total_volumes']]
new_df_cardano = another_dataframe_cardano.copy()


df_cardano['date'] = [i[:10] for i in df_cardano['date']]


df_cardano['day'] = pd.DatetimeIndex(df_cardano['date']).day_name()

df_one_day_cardano = df.groupby(df['date']).sum().reset_index()

start_date_cardano = new_df_cardano['date'][0]
end_date_cardano = new_df_cardano['date'].to_list()[-1]


dict_main = {'Bitcoin': new_df, 'Ethereum': new_df_ethereum, 'Cardano': new_df_cardano}
#---------------------------------------------------------------------------------

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(
#   __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
#)
app = dash.Dash(__name__)
app.title = "Cryptocurrency Data Visualisation"
server = app.server


rpm = list(dict_main.keys())
channels = dict_main[rpm[0]]

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",

)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Bitcoin Data Visualisation",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "from "+start_date+' to '+end_date, style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                           "Filter by date",
                            className="control_label",
                        ),
                        # dcc.RangeSlider(
                        #    id="year_slider",
                        #    min=1960,
                        #    max=2017,
                        #    value=[1990, 2010],
                        #    className="dcc_control",
                        #),
                        
                           
                       # html.P("Select the date", className="control_label"),

                        
                        #html.P("Select", className="control_label"),
        dcc.Dropdown(
            id='rpm-dropdown',
            options=[{'label':speed, 'value':speed} for speed in rpm],
            value=list(dict_main.keys())[0],
            searchable=True
            ),
        html.Br(),
        
        
        
                dcc.Dropdown(
            id='channel-dropdown',
            multi=True,
            ),
       
 
                
                   
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                
                                      
                
                html.Div(
                    [
              
                        html.Div(
                            [
                       
                                html.Div(
                                    [html.P("Maximum price was "+ str(round(max_price))+ ' on '+ str(date_of_max_price))],
                                    id="max_price",
                                    className="mini_container",
                                ),
                                
                                  html.Div(
                                    [html.P("Maximum total volume was "+ str(round(max_total_volume))+ ' on '+ str(date_of_max_total_volume))],
                                    id="max_total_volume",
                                    className="mini_container",
                                ),
                                  
                                   html.Div(
                                    [html.P("Maximum market cap was "+ str(round(max_market_caps))+ ' on '+ str(date_of_max_market_caps))],
                                    id="max_market_caps",
                                    className="mini_container",
                                ),
                              
                         
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        
                        
                        html.Div(
                            [
         
                                html.Div(
                                    [html.P("Minimum price was "+ str(round(min_price))+ ' on '+ str(date_of_min_price))],
                                    id="min_price",
                                    className="mini_container",
                                ),
                                
                                 html.Div(
                                    [html.P("Minimum total volume was "+ str(round(min_total_volume))+ ' on '+ str(date_of_min_total_volume))],
                                    id="min_total_volume",
                                    className="mini_container",
                                ),
                                  
                                   html.Div(
                                    [html.P("Minimum market cap was "+ str(round(min_market_caps))+ ' on '+ str(date_of_min_market_caps))],
                                    id="min_market_caps",
                                    className="mini_container",
                                ),

                           
                            ],
                            id="info-container1",
                            className="row container-display",
                        ),
                        
                        
 
                        html.Div(
                            [dcc.Graph(id="the_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        


    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


#----------------------------------------------------------------------------------------

@app.callback(
    Output('channel-dropdown', 'options'),
    [Input('rpm-dropdown', 'value')])
def update_date_dropdown(speed):
    #return [{'label': i, 'value': i} for i in dict_main[speed]]
    return [{'label': i, 'value': i} for i in dict_main[speed].drop(columns = 'date')]



@app.callback(
    Output('the-graph', 'figure'),
    [Input('channel-dropdown', 'value')],
    [State('rpm-dropdown', 'value')])
def updateGraph(channels, test):
    if channels:
        return go.Figure(data=[go.Scatter(x=dict_main[test]['date'], y=dict_main[test][i], name=i) for i in channels])
    else:
        return go.Figure(data=[])


# Main
if __name__ == "__main__":
    app.run_server(port =8050)