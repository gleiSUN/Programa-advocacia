import dash
import plotly.express as px
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc

import json
import pandas as pd

from components import modal_novo_processo, modal_novo_advogado, modal_advogados
from app import app

# ========= Layout ========= #
import dash_bootstrap_components as dbc

# Add FontAwesome CSS link to ensure icons load
fontawesome_link = html.Link(href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css", rel="stylesheet")

layout = dbc.Container([
    # Include FontAwesome link at the top to ensure icons appear
    fontawesome_link,
    
    # Modals remain unchanged
    modal_novo_processo.layout,
    modal_novo_advogado.layout,
    modal_advogados.layout,
    
    # Main header container with improved styling: dark gray background, red accents
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("LEXManager", 
                        style={
                            'color': '#FF0000',  # Bright red for title
                            'text-shadow': '2px 2px 4px #000000',  # Black shadow for depth
                            'font-weight': 'bold',
                            'font-family': 'Arial, sans-serif'
                        })
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("ASSOCIATES", 
                        style={
                            'color': '#FFFFFF',  # White for subtitle
                            'text-shadow': '1px 1px 2px #000000'  # Subtle black shadow
                        })
            ]),
        ]),
    ], 
    style={
        'padding-top': '50px', 
        'margin-bottom': '100px', 
        'background-color': '#333333',  # Dark gray background
        'border-radius': '10px',  # Rounded corners for modern look
        'box-shadow': '0 4px 8px rgba(0,0,0,0.5)'  # Shadow for depth
    }, 
    className='text-center'),
    
    # Horizontal rule with red color
    html.Hr(style={'border-color': '#FF0000', 'border-width': '2px'}),
    
    # Navigation row with improved styling
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink([
                    html.I(className='fas fa-home', style={'color': '#FF0000', 'margin-right': '10px'}),  # Red home icon
                    "INÍCIO"
                ], href="/home", active=True, 
                style={
                    'text-align': 'left', 
                    'color': '#FFFFFF',  # White text
                    'background-color': '#333333',  # Dark gray background
                    'border-radius': '5px',
                    'padding': '10px',
                    'margin-bottom': '10px'
                })),
                dbc.NavItem(dbc.NavLink([
                    html.I(className='fas fa-plus-circle', style={'color': '#FF0000', 'margin-right': '10px'}),  # Red plus icon
                    "PROCESSOS"
                ], id='processo_button', active=True, 
                style={
                    'text-align': 'left', 
                    'color': '#FFFFFF',
                    'background-color': '#333333',
                    'border-radius': '5px',
                    'padding': '10px',
                    'margin-bottom': '10px'
                })),
                dbc.NavItem(dbc.NavLink([
                    html.I(className='fas fa-user-plus', style={'color': '#FF0000', 'margin-right': '10px'}),  # Red user-plus icon
                    "ADVOGADOS"
                ], id='lawyers_button', active=True, 
                style={
                    'text-align': 'left', 
                    'color': '#FFFFFF',
                    'background-color': '#333333',
                    'border-radius': '5px',
                    'padding': '10px',
                    'margin-bottom': '10px'
                })),
                
                # ✅ BOTÃO DE LOGOUT ADICIONADO DENTRO DO NAV
                dbc.NavItem(dbc.NavLink([
                    html.I(className='fas fa-sign-out-alt', style={'color': '#FF0000', 'margin-right': '10px'}),
                    "SAIR"
                ], id='logout-button', active=True, 
                style={
                    'text-align': 'left', 
                    'color': '#FFFFFF',
                    'background-color': '#333333',
                    'border-radius': '5px',
                    'padding': '10px',
                    'margin-top': '20px'  # Espaço acima do botão
                })),
            ], 
            vertical="lg", 
            pills=True, 
            fill=True,
            style={'background-color': '#333333', 'padding': '20px', 'border-radius': '10px'}  # Dark gray nav background
            )
        ])
    ]),
], 
style={
    'height': '100vh', 
    'padding': '0px', 
    'position': 'sticky', 
    'top': 0, 
    'background-color': '#333333'  # Overall dark gray background
})

# ======= Callbacks ======== #
# Abrir Modal New Lawyer
@app.callback(
    Output('modal_new_lawyer', "is_open"),
    Input('new_adv_button', 'n_clicks'),
    Input("cancel_button_novo_advogado", 'n_clicks'),
    State('modal_new_lawyer', "is_open")
)
def toggle_modal(n, n2, is_open):
    if n or n2:
        return not is_open
    return is_open

# Abrir Modal Lawyers
@app.callback(
    Output('modal_lawyers', "is_open"),
    Input('lawyers_button', 'n_clicks'),
    Input('quit_button', 'n_clicks'),
    Input('new_adv_button', 'n_clicks'),
    State('modal_lawyers', "is_open")
)
def toggle_modal(n, n2, n3, is_open):
    if n or n2 or n3:
        return not is_open
    return is_open