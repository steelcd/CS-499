# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import Dash
from dash import html
import plotly.express as px
from dash import dash_table
from dash import no_update
from dash.dependencies import Input, Output, State
import base64
import requests

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

table_columns = [
            {'name': 'Shelter', 'id': 'shelter'},
            {'name': 'Animal ID', 'id': 'animal_id'},
            {'name': 'Name', 'id': 'name'},
            {'name': 'Type', 'id': 'animal_type'},
            {'name': 'Breed', 'id': 'breed'},
            {'name': 'date_of_birth', 'id': 'DOB'},
            {'name': 'Outcome', 'id': 'outcome_type'},
            {'name': 'Sex', 'id': 'sex_upon_outcome'}
            ]

score_column = {'name': 'Score', 'id': 'score'}


# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
#df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
#df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = Dash(
    __name__,
    requests_pathname_prefix='/dashboard/',
    routes_pathname_prefix='/'
)

image_filename = 'grazioso_salvare_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Create function to refresh data and then return layout
def serve_layout():

    # Fetch data
    response = requests.get("http://nodejs:3000/api/animals")
    json_data = response.json()
    df = pd.DataFrame(json_data)
    df.drop(columns=['_id'], inplace=True, errors='ignore')

    return html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('CS-340 Dashboard', style={'marginTop': '10px'}))),
    html.Div(className='row',
         style={'display' : 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
             children=[
                 html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                          style={'height':'6%', 'width':'6%'}),
                 html.Center(html.H2('Module 7 - Project 2 - Chris Stevens'))
             ]
    ),           
    html.Hr(),
    html.Div(className='row',
             style={'display': 'flex', 'alignItems': 'center'},
             children=[
        html.Div([
            dcc.Dropdown(
                id='filter-type',
                value ='all',
                clearable=False,
                options=[
                    {'label': 'All animals', 'value': 'all'},
                    {'label': 'Water', 'value': 'water'},
                    {'label': 'Mountain or Wilderness', 'value': 'mountain_wilderness'},
                    {'label': 'Disaster or Individual Tracking', 'value': 'disaster_tracking'}

        ],
        style={'width': '100%'}),
        html.Div(
            html.Button(
                id='clear_filters',
                n_clicks=0,
                children='Clear filter(s)'
            ),
            style={'marginLeft': '12px'}
        )
        ],
        style={'display': 'flex', 'alignItems': 'center', 'width': '420px'}),
             ]
             ),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=table_columns,
        data=df.to_dict('records'),
        row_selectable='single',
        filter_action='native',
        sort_action='native',
        sort_by=[{"column_id": "rec_num", "direction": "asc"}],
        page_action='native',
        page_size=50,
        style_table={'height': '250px', 'overflowY': 'auto'}
    ),
    html.Br(),
    html.Hr(),
    #This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            style={'width': '50%', 'padding':'10px'}

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            style={'width': '50%', 'padding':'10px'}
            )
        ])
    ])

app.layout = serve_layout

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(
    Output('filter-type', 'value'),
    [Input('clear_filters', 'n_clicks')],
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return 'all'

@app.callback(Output('datatable-id','data'),
              Output('datatable-id', 'columns'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    
    if filter_type == 'all':
        columns = table_columns
        
        # Fetch data
        response = requests.get(f"http://nodejs:3000/api/animals")
        json_data = response.json()
        df = pd.DataFrame(json_data)
        df.drop(columns=['_id'], inplace=True, errors='ignore')

    else:

        columns = [score_column] + table_columns

        # Fetch data
        response = requests.get(f"http://nodejs:3000/api/rescue-candidates/{filter_type}")
        json_data = response.json()
        df = pd.DataFrame(json_data)
        df.drop(columns=['_id'], inplace=True, errors='ignore')

    return df.to_dict('records'), columns

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    df = pd.DataFrame.from_dict(viewData)
    breed_df = df.get('breed')
    
    if not viewData:
        value_counts = pd.DataFrame(columns=['breed', 'total'])
        
    else:
    
        if breed_df is not None:

            value_counts = df['breed'].value_counts().reset_index()
            value_counts.columns= ['breed', 'total']

        else:

            value_counts = pd.DataFrame(columns=['breed', 'total'])
    
    return [
        dcc.Graph(            
            figure = px.bar(value_counts, x='breed', y='total', title='Breed count')
        )    
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'derived_viewport_selected_rows')]
)
def update_styles(viewport_selected_rows):
    if viewport_selected_rows is None:
        return no_update
    return [{
        'if': { 'row_index': viewport_selected_rows[0] },
        'background_color': '#D2F3FF'
    } for i in viewport_selected_rows]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
     Input('datatable-id', "derived_viewport_selected_rows")])
def update_map(viewData, viewport_selected_rows):
    dff = pd.DataFrame.from_dict(viewData)
    
    if dff.empty:
        return [html.Div('No data available')]
    
    row = viewport_selected_rows[0] if viewport_selected_rows else 0
    lat = dff.iloc[row]['location_lat']
    lon = dff.iloc[row]['location_long']
    
    return [
        dl.Map(style={'height': '400px'},
               scrollWheelZoom=False,
               zoomControl=True,
              center=[lat,lon], zoom=10, children=[
                  dl.TileLayer(id='base-layer-id'),
                  dl.Marker(position=[lat, lon],
                           children=[
                               dl.Tooltip(dff.iloc[row]['breed']),
                               dl.Popup([
                                   html.H1('Animal Name'),
                                   html.P(dff.iloc[row]['name'])
                               ])
                           ])
              ])
    ]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
