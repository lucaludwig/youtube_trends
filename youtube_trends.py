#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output
from datetime import datetime


# In[2]:

data = pd.read_csv('/home/visualanalytics/mysite/data.csv', delimiter=",")
data_coun_cat = pd.read_csv('/home/visualanalytics/mysite/data_coun_cat.csv', delimiter=",")
data_count = pd.read_csv('/home/visualanalytics/mysite/data_count.csv', delimiter=",")
data_cat_eng = pd.read_csv('/home/visualanalytics/mysite/data_cat_eng.csv', delimiter=",")
data_trend = pd.read_csv('/home/visualanalytics/mysite/data_trend.csv', delimiter=",")
cat_minmax = pd.read_csv('/home/visualanalytics/mysite/cat_minmax.csv', delimiter=",")


# In[3]:


views = data["views"]
count = data["count"]
category = data['category']
cat_order = data.sort_values(by=['count'], ascending=False)
cat_order_list = cat_order['category']

fig1 = go.Figure(
    data=[
        go.Bar(name='Count', x=category, y=count, yaxis='y', offsetgroup=1, marker_color='navy'),
        go.Bar(name='Views', x=category, y=views, yaxis='y2', offsetgroup=2)
    ],
    layout={
        'yaxis': {'title': 'Count Axis'},
        'yaxis2': {'title': 'Views Axis', 'overlaying': 'y', 'side': 'right'},
        'xaxis': {'categoryarray' : cat_order_list, 'categoryorder':'array'}
    }
)

# Change the bar mode
fig1.update_layout(barmode='group')
fig1.update_layout(
title="Popularity of Categories",title_x=0.5)
fig1.update_layout(
            title={
            'yanchor': 'top'
        }
)

fig1.update_layout(legend=dict(
    xanchor="left",
    x=0.8532
))



z = np.log10(data_coun_cat['like/dislike'])
fig2 = px.choropleth(data_coun_cat, locations="alpha3",
color=z, # lifeExp is a column of gapminder
hover_name="country", # column to add to hover information
color_continuous_scale="ylorbr",
title="Popularity of Categories per Country")
#Focus on map filled with data
fig2.update_geos(fitbounds="locations")
fig2.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig2.update_layout(height=400, margin={"r":0,"t":20,"l":0,"b":100})
fig2.update_layout(coloraxis_colorbar=dict(
    title="Like/Dislike Ratio"))
fig2.update_layout(title={'yanchor':'top'}, title_x=0.18, title_y = 0.995)



fig3 = px.bar(data_cat_eng, x="comtoview", y="category", orientation='h', log_x=True, barmode="group",labels={"comtoview": "Comment/View Ratio", "category": "Categories", "value": ""}, title="User Engagement")
fig3.update_traces(width=0.6)
fig3.update_traces(marker_color='rgb(0,100,0)', marker_line_color='rgb(0,100,0)',
                opacity=0.8)
fig3.update_layout(title={'yanchor': 'top'}, title_x=0.5)
fig3.update_yaxes(categoryorder='total ascending')


cat = data_coun_cat.category.unique()
cat = cat.tolist()

fig4 = px.line(data_trend, x = "trending_date", y = "trend_count", color ="category",log_y=True,labels={"category": "Legend", "trend_count": "Number of Videos in Youtube Trends", "trending_date": "Trending Date"}, title="Trending Videos per Month")
#fig4.update_layout(hovermode="x unified")
fig4.update_layout(title={'yanchor': 'top'}, title_x=0.45)


# In[4]:


fig5 = go.Figure()

fig5.add_trace(go.Indicator(
    mode = "number",
    value = sum(data['count']),
    title = {'text': "Videos", 'font': {"size": 30},},
    domain = {'row': 0, 'column': 0},
    number={"font":{"size":60}}))

fig5.add_trace(go.Indicator(
    mode = "number",
    value = (len(data['category'])),
    title = {'text': "Categories", 'font': {"size": 30},},
    domain = {'row': 0, 'column': 1},
    number={"font":{"size":60}}))

fig5.add_trace(go.Indicator(
    mode = "number",
    value = (len(list(set(data_coun_cat['alpha3'])))),
    title = {'text': "Countries", 'font': {"size": 30},},
    domain = {'row': 0, 'column': 2},
    number={"font":{"size":60}}))

sdate = datetime.fromisoformat(min(cat_minmax['amin']))
edate = datetime.fromisoformat(max(cat_minmax['amax']))
delta = edate - sdate

fig5.add_trace(go.Indicator(
    mode = "number",
    value = delta.days,
    title = {'text': 'Days', 'font': {"size": 30},},
    domain = {'row': 0, 'column': 3},
    number={"font":{"size":60}}))

fig5.update_layout(
    grid = {'rows': 1, 'columns': 4, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
#        'title': {'text': "Videos"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})
fig5.update_layout(
    paper_bgcolor="lightgray",
    height=200,  # Added parameter
)


# In[5]:


app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Youtube Trend Analytics", style={'textAlign': 'center'}, className="header")
            ],
            className="header",
        ), #Description below the header

        html.Div(
            children=[
                html.Div(children = 'Category', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'cat-filter',
                    options = [
                        {'label': category, 'value': category}
                        for category in data_coun_cat.category.unique()
                    ], #'Year' is the filter
                    value = '',
                    clearable = True,
                    searchable = True,
                    multi = True,
                    className = 'dropdown', style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu',
        ), #the dropdown function


        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'fig5',
                    figure = fig5,
                  #  config={"displayModeBar": False},
                ),
                style={'width': '100%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'bar1',
                    figure = fig1,
                  #  config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'scatter',
                    figure = fig2,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'}
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'fig3',
                    figure = fig3,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
                html.Div(
                children = dcc.Graph(
                    id = 'fig4',
                    figure = fig4,
                    #config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            )
        ],
        className = 'double-graph',
        ),
    ]
)


# In[6]:


@app.callback(
    Output("scatter", "figure"), #the output is the scatterchart
    [Input("cat-filter", "value")], #the input is the year-filter
)
def update_charts(category):
    if cat in category:
        filtered_data = data_coun_cat.copy()
    else:
        filtered_data = data_coun_cat[data_coun_cat["category"].isin(category)]

    z = np.log10(filtered_data['like/dislike'])
    scatter = px.choropleth(filtered_data, locations="alpha3",
                        color=z, # lifeExp is a column of gapminder
                        hover_name="alpha3", # column to add to hover information
                        color_continuous_scale="ylorbr", title="Popularity of Categories per Country")
    #Focus on map filled with data
    scatter.update_geos(fitbounds="locations")
    scatter.update_layout(height=400, margin={"r":0,"t":20,"l":0,"b":100})
    scatter.update_layout(coloraxis_colorbar=dict(
    title="Like/Dislike Ratio"))
    scatter.update_layout(
            title={
            'yanchor': 'top'
        }, title_x = 0.18, title_y = 0.995)

    return scatter #return the scatterchart according to the filter

@app.callback(
    Output("bar1", "figure"), #the output is the scatterchart
    [Input("cat-filter", "value")], #the input is the year-filter
)

def update_charts(category):
    if cat in category:
        filtered_data = data.copy()
    else:
        filtered_data = data[data["category"].isin(category)]

    views = filtered_data["views"]
    count = filtered_data["count"]
    category = filtered_data['category']
    cat_order = filtered_data.sort_values(by=['count'], ascending=False)
    cat_order_list = cat_order['category']

    bar1 = go.Figure(
        data=[
            go.Bar(name='Count', x=category, y=count, yaxis='y', offsetgroup=1, marker_color='navy'),
            go.Bar(name='Views', x=category, y=views, yaxis='y2', offsetgroup=2)
        ],
        layout={
            'yaxis': {'title': 'Count Axis'},
            'yaxis2': {'title': 'Views Axis', 'overlaying': 'y', 'side': 'right'},
            'xaxis': {'categoryarray' : cat_order_list, 'categoryorder':'array'}
        }
    )

    # Change the bar mode
    bar1.update_layout(barmode='group')

    bar1.update_layout(
        title="Popularity of Categories")
    bar1.update_layout(
                title={
                'yanchor': 'top'
            }, title_x=0.5)

    bar1.update_layout(legend=dict(
    xanchor="left",
    x=0.8532
))



    return bar1 #return the scatterchart according to the filter

@app.callback(
    Output("fig3", "figure"), #the output is the scatterchart
    [Input("cat-filter", "value")], #the input is the year-filter
)

def update_charts(category):
    if cat in category:
        filtered_data = data_cat_eng.copy()
    else:
        filtered_data = data_cat_eng[data_cat_eng["category"].isin(category)]

    fig3 = px.bar(filtered_data, x="comtoview", y="category", orientation='h', log_x=True, barmode="group",labels={"comtoview": "Comment/View Ratio", "category": "Categories", "value": ""}, title="User Engagement")
    fig3.update_traces(width=0.6)
    fig3.update_traces(marker_color='rgb(0,100,0)', marker_line_color='rgb(0,100,0)',
                    opacity=0.8)
    fig3.update_layout(
            title={
            'yanchor': 'top'
        }, title_x=0.5)
    fig3.update_yaxes(categoryorder='total ascending')

    return fig3 #return the scatterchart according to the filter

@app.callback(
    Output("fig4", "figure"), #the output is the scatterchart
    [Input("cat-filter", "value")], #the input is the year-filter
)

def update_charts(category):
    if cat in category:
        filtered_data = data_trend.copy()
    else:
        filtered_data = data_trend[data_trend["category"].isin(category)]

    fig4 = px.line(filtered_data, x = "trending_date", y = "trend_count", color ="category",log_y=True,labels={"category": "Legend", "trend_count": "Number of Videos in Youtube Trends", "trending_date": "Trending Date"}, title="Trending Videos per Month")
    #fig4.update_layout(hovermode="x unified")
    fig4.update_layout(
            title={
            'yanchor': 'top'
        }, title_x=0.45)
    return fig4 #return the scatterchart according to the filter

@app.callback(
    Output("fig5", "figure"), #the output is the scatterchart
    [Input("cat-filter", "value")], #the input is the year-filter
)

def update_charts(category):
    if cat in category:
        filtered_data_1 = data.copy()
        filtered_data_2 = data_coun_cat.copy()
        filtered_data_3 = cat_minmax.copy()
    else:
        filtered_data_1 = data[data["category"].isin(category)]
        filtered_data_2 = data_coun_cat[data_coun_cat["category"].isin(category)]
        filtered_data_3 = cat_minmax[cat_minmax["category"].isin(category)]

    fig5 = go.Figure()

    fig5.add_trace(go.Indicator(
        mode = "number",
        value = sum(filtered_data_1['count']),
        title = {'text': "Videos", 'font': {"size": 30},},
        domain = {'row': 0, 'column': 0},
        number={"font":{"size":60}}))

    fig5.add_trace(go.Indicator(
        mode = "number",
        value = (len(filtered_data_1['category'])),
        title = {'text': "Categories", 'font': {"size": 30},},
        domain = {'row': 0, 'column': 1},
        number={"font":{"size":60}}))

    fig5.add_trace(go.Indicator(
        mode = "number",
        value = (len(list(set(filtered_data_2['alpha3'])))),
        title = {'text': "Countries", 'font': {"size": 30},},
        domain = {'row': 0, 'column': 2},
        number={"font":{"size":60}}))

    sdate = datetime.fromisoformat(min(filtered_data_3['amin']))
    edate = datetime.fromisoformat(max(filtered_data_3['amax']))
    delta = edate - sdate

    fig5.add_trace(go.Indicator(
        mode = "number",
        value = delta.days,
        title = {'text': 'Days', 'font': {"size": 30},},
        domain = {'row': 0, 'column': 3},
        number={"font":{"size":60}}))

    fig5.update_layout(
        grid = {'rows': 1, 'columns': 4, 'pattern': "independent"},
        template = {'data' : {'indicator': [{
    #        'title': {'text': "Videos"},
            'mode' : "number+delta+gauge",
            'delta' : {'reference': 90}}]
                             }})
    fig5.update_layout(
        paper_bgcolor="lightgray",
        height=200,  # Added parameter
    )

    return fig5 #return the scatterchart according to the filter


# In[ ]:


if __name__ == "__main__":
    app.run_server(debug=False, use_reloader=False)


# In[ ]:





# In[ ]:




