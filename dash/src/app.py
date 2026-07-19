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

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from animalshelter import AnimalShelter

#FIXME Data is loaded at app start, page will never get new data how that it's being hosted
# as a continuing service

###########################
# Data Manipulation / Model
###########################


# Update with your credentials
username = "mongo_user"
password = "mongo_password"

# Connect to database via CRUD Module
host = 'mongo'
port = 27017
db = 'aac'
collection = 'animals'
db = AnimalShelter(
    username,
    password,
    host,
    port,
    db,
    collection
)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

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

app.layout = html.Div([
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
                options=['Water', 'Mountain or Wilderness', 'Disaster or Individual Tracking'],
                placeholder='Select a rescue type')
        ],
        style={'width': '30%'}),
        html.Div(html.Button(id='clear_filters', n_clicks=0, children='Clear filter(s)'))
             ]
            ),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
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

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    
    print(filter_type)
    # Filters by selection value
    filter_dict = {
        'Water': {'animal_type': 'Dog',
                'breed': {'$in' :['Labrador Retriever Mix',
                                    'Chesapeake Bay Retriever',
                                    'Chesa Bay Retr',
                                    'Newfoundland']
                           },
                 'sex_upon_outcome': 'Intact Female',
                 'age_upon_outcome_in_weeks': {'$gte':26, '$lte':156}
                 },
        'Mountain or Wilderness': {'animal_type': 'Dog',
                'breed': {'$in' :['German Shepherd',
                                                     'Alaskan Malamute',
                                                     'Old English Sheepdog',
                                                    'Siberian Husky',
                                                    'Rottweiler']},
                 'sex_upon_outcome': 'Intact Male',
                 'age_upon_outcome_in_weeks': {'$gte':26, '$lte':156}
                 },
        'Disaster or Individual Tracking': {'animal_type': 'Dog',
                'breed': {'$in' :['Doberman Pinscher',
                                                    'Doberman Pinsch',
                                                     'German Shepherd',
                                                     'Golden Retriever',
                                                    'Bloodhound',
                                                    'Rottweiler']},
                 'sex_upon_outcome': 'Intact Male',
                 'age_upon_outcome_in_weeks': {'$gte':20, '$lte':300}
                 }
    }
    
    filter = filter_dict.get(filter_type, None)
    
    if filter is None:
        df = pd.DataFrame.from_records(db.read({}))
    else:
        df = pd.DataFrame.from_records(db.read(filter))
        
    #Clean up id field, handle no records return from filter
    if len(df) > 0:
        df.drop(columns=['_id'],inplace=True)
    
    return df.to_dict('records')    

# Clear filters from dropdown and table
@app.callback(
    Output('filter-type', 'value'),
    Output('datatable-id', 'filter_query'),
    [Input('clear_filters', 'n_clicks')])
def clear_filters(n_clicks):
    if n_clicks:
        dropdown_return = ''
        table_return = ''
        
        return dropdown_return, table_return
    else:
        return no_update, no_update

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
