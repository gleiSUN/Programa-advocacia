import dash
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from dash import dash_table
from dash.dash_table.Format import Group

from app import app
from components import home

# ======== Layout ========= #
import dash_bootstrap_components as dbc


layout = dbc.Modal([
    dbc.ModalHeader(
        dbc.ModalTitle([
            html.I(className='fas fa-gavel', style={'margin-right': '10px', 'color': '#FF0000'}),  # Red gavel icon for legal theme
            "Cadastro de Advogados"
        ], 
        style={
            'color': '#FF0000',  # Red title
            'text-shadow': '2px 2px 4px #000000',  # Strong black shadow for emphasis
            'font-weight': 'bold',
            'font-size': '24px'  # Larger font for impact
        }),
        style={'background-color': '#333333', 'border-bottom': '3px solid #FF0000', 'border-radius': '10px 10px 0 0'}  # Gray header with thicker red border and rounded top
    ),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                html.Div(id='table_adv', className="dbc", 
                         style={
                             'background-color': '#333333', 
                             'color': '#FFFFFF', 
                             'padding': '20px', 
                             'border-radius': '10px',
                             'box-shadow': 'inset 0 2px 4px rgba(0,0,0,0.3)',  # Inner shadow for depth
                             'min-height': '300px'  # Ensure space for table
                         })  # Enhanced gray background with padding and shadow
            ]),
        ])
    ], style={'background-color': '#333333', 'color': '#FFFFFF', 'padding': '20px'}),  # Gray body with more padding
    dbc.ModalFooter([
        dbc.Button([
            html.I(className='fas fa-times-circle', style={'margin-right': '8px', 'color': '#FFFFFF'}),  # White close icon with circle
            "Sair"
        ], id="quit_button", 
        style={
            'background-color': '#FF0000', 
            'border-color': '#FF0000', 
            'color': '#FFFFFF',
            'border-radius': '5px',
            'font-weight': 'bold'
        },  # Bold red button
        color="danger"),
        dbc.Button([
            html.I(className='fas fa-plus-circle', style={'margin-right': '8px', 'color': '#FF0000'}),  # Red plus icon with circle
            "Novo"
        ], id="new_adv_button", 
        style={
            'background-color': '#333333', 
            'border-color': '#FF0000', 
            'color': '#FFFFFF',
            'border-radius': '5px',
            'font-weight': 'bold'
        },  # Gray button with red border
        color="success")
    ], style={'background-color': '#333333', 'border-top': '3px solid #FF0000', 'border-radius': '0 0 10px 10px'})  # Gray footer with thicker red border and rounded bottom
], id="modal_lawyers", size="lg", is_open=False, 
style={
    'background-color': '#333333', 
    'border-radius': '10px', 
    'box-shadow': '0 8px 16px rgba(0,0,0,0.7)',  # Stronger shadow for modal
    'border': '2px solid #FF0000'  # Red border around entire modal
})



# ====== Callbacks ======= #
# Tabela com os advogados da empresa
@app.callback(
    Output('table_adv', 'children'),
    Input('store_adv', 'data')
    # Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def table(data):
    df = pd.DataFrame(data)

    df = df.fillna('-')
    return [dash_table.DataTable(
        id='datatable',
        columns = [{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single", 
        page_size=10,            
        page_current=0)]
