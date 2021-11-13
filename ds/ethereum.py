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
import dash_table

import plotly.graph_objects as go



#--------------------------------------------Data-----------------------------------





data_requests = requests.get(
        "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=30"
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

mc_last_price = "{:,}".format(round(df['market_caps'].to_list()[-1]))
tv_last_price = "{:,}".format(round(df['total_volumes'].to_list()[-1]))
#---------------------------------------------------------------------------------


fig_price = go.Figure(go.Indicator(
    mode = "number+delta",
    value = df['prices'].to_list()[-1],
    number = {'prefix': "$"},
    delta = {'position': "top", 'reference': df['prices'].to_list()[-2]},
    domain = {'x': [0, 1], 'y': [0, 1]}))
fig_price.update_traces(delta_font={'size':13}, number_font={'size':18})
fig_price.update_layout(paper_bgcolor = "#f9f9f9", height=50, width=100)

fig_price.show()


fig_mc = go.Figure(go.Indicator(
    mode = "number+delta",
    value = df['market_caps'].to_list()[-1],
    number = {'prefix': "$"},
    delta = {'position': "top", 'reference': df['market_caps'].to_list()[-2]},
    domain = {'x': [0, 1], 'y': [0, 1]}))
fig_mc.update_traces(delta_font={'size':13}, number_font={'size':18})
fig_mc.update_layout(paper_bgcolor = "#f9f9f9", height=50, width=100)

fig_mc.show()


fig_tv = go.Figure(go.Indicator(
    mode = "number+delta",
    value = df['total_volumes'].to_list()[-1],
    number = {'prefix': "$"},
    delta = {'position': "top", 'reference': df['total_volumes'].to_list()[-2]},
    domain = {'x': [0, 1], 'y': [0, 1]}))
fig_tv.update_traces(delta_font={'size':13}, number_font={'size':18})
fig_tv.update_layout(paper_bgcolor = "#f9f9f9", height=50, width=100)

fig_tv.show()

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Ethereum Data Visualisation"
server = app.server

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
                                    "Ethereum Data Visualisation",
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
                        dcc.RadioItems(
                            id="xaxis_raditem",
                            options=[
                              {'label': 'Date', 'value': 'date'}
                            ],
                            value="date",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        
                        #html.P("Select", className="control_label"),
                        dcc.RadioItems(
                            id="yaxis_raditem",
                            options=[
                               {'label': 'Market caps  ', 'value': 'market_caps'},
                               {'label': 'Prices  ', 'value': 'prices'},
                               {'label': 'Total volumes  ', 'value': 'total_volumes'},
                            ],
                            value="prices",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="y-dropdown",
                            options = [
                            {'label':'Mean market cap', 'value': 'mean_market_caps'},
                            {'label':'Mean price', 'value': 'mean_prices'},
                            {'label':'Mean total volume', 'value': 'mean_total_volumes'}],
                            multi=False,
                            value='mean_prices',
                            className="dcc_control",
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
                             
                            [dcc.Graph(figure=fig_price)],
                            id="indicator_price",
                            className="mini_container",
                        ),
                                
                                    html.Div(
                                       
                                    [html.P("Market cap     $"+ str(mc_last_price))],
                                    id="market_cap",
                                    className="mini_container",
                                ),
                                    
                                    html.Div(
                                       
                                    [html.P("24 Hour Trading Vol     $"+ str(tv_last_price))],
                                    id="total_volume",
                                    className="mini_container",
                                ),
                                

                                
                                
                         
                            ],
                            id="info-container",
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
        
        
        
        
        
        
        
        
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="the_chart")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="the_bar_chart")],
                    className="pretty_container five columns",
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
    Output(component_id='the_chart', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)

def update_graph(x_axis, y_axis):

    dff = df

    barchart=px.bar(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            title=y_axis+' by '+x_axis,
            
            )

    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,},
                           # template='plotly_dark',
                       plot_bgcolor= '#f9f9f9',
                       paper_bgcolor= '#f9f9f9'
                        )
   

    return (barchart)

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)

def build_graph(x_axis, y_axis):
    dff = new_df

    fig = px.line(dff, x=x_axis, y=y_axis, height=450)
    fig.update_layout(yaxis={'title':y_axis},
                      title={'text':y_axis+' by '+x_axis,
                      'font':{'size':17},'x':0.5,'xanchor':'center'},
                      
                       #template='plotly_dark',
                     plot_bgcolor= '#f9f9f9',
                     paper_bgcolor= '#f9f9f9'
                       )
    return fig


@app.callback(
    Output(component_id='the_bar_chart', component_property='figure'),
    [
     Input(component_id='y-dropdown', component_property='value')]
)

def bar_graph(y_axis):

    dff = df_mean

    barchart2=px.bar(
            data_frame=dff,
            x=df_mean['days'],
            y=y_axis,
            title=y_axis,
      
            
            
            )

    barchart2.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5},
                       
                           
                          # template='plotly_dark',
            plot_bgcolor= '#f9f9f9',
            paper_bgcolor= '#f9f9f9'
            )

    return (barchart2)





# Main
if __name__ == "__main__":
    app.run_server(port =1234)