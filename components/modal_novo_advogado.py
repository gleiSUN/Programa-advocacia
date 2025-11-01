import dash
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from app import app

# ========= Layout ========= #


# Add FontAwesome CSS link to ensure icons load (if not already in your app)
fontawesome_link = html.Link(href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css", rel="stylesheet")

layout = dbc.Modal([
    # Include FontAwesome link at the top to ensure icons appear
    fontawesome_link,
    
    dbc.ModalHeader(
        dbc.ModalTitle([
            html.I(className='fas fa-user-plus', style={'margin-right': '10px', 'color': '#FF0000'}),  # Red user-plus icon
            "Adicione Um Advogado"
        ], 
        style={
            'color': '#FF0000',  # Red title
            'text-shadow': '2px 2px 4px #000000',  # Black shadow for depth
            'font-weight': 'bold',
            'font-size': '24px'  # Larger font for impact
        }),
        style={'background-color': '#333333', 'border-bottom': '3px solid #FF0000', 'border-radius': '10px 10px 0 0'}  # Gray header with red border and rounded top
    ),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("OAB", style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.Input(id="adv_oab", placeholder="Apenas números, referente a OAB...", type="number", 
                          style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White input with red border
            ], sm=12, md=6),
            dbc.Col([
                dbc.Label("CPF", style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.Input(id="adv_cpf", placeholder="Apenas números, CPF...", type="number", 
                          style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White input with red border
            ], sm=12, md=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Nome", style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.Input(id="adv_nome", placeholder="Nome completo do advogado...", type="text", 
                          style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White input with red border
            ]),
        ]),
        html.H5(id='div_erro2', style={'color': '#FF0000', 'text-align': 'center', 'margin-top': '20px'})  # Red error message, centered
    ], style={'background-color': '#333333', 'color': '#FFFFFF', 'padding': '20px'}),  # Gray body with padding
    dbc.ModalFooter([
        dbc.Button([
            html.I(className='fas fa-times', style={'margin-right': '8px', 'color': '#FFFFFF'}),  # White close icon
            "Cancelar"
        ], id="cancel_button_novo_advogado", 
        style={
            'background-color': '#FF0000', 
            'border-color': '#FF0000', 
            'color': '#FFFFFF',
            'border-radius': '5px',
            'font-weight': 'bold'
        },  # Red button
        color="danger"),
        dbc.Button([
            html.I(className='fas fa-save', style={'margin-right': '8px', 'color': '#FF0000'}),  # Red save icon
            "Salvar"
        ], id="save_button_novo_advogado", 
        style={
            'background-color': '#333333', 
            'border-color': '#FF0000', 
            'color': '#FFFFFF',
            'border-radius': '5px',
            'font-weight': 'bold'
        },  # Gray button with red border
        color="success")
    ], style={'background-color': '#333333', 'border-top': '3px solid #FF0000', 'border-radius': '0 0 10px 10px'})  # Gray footer with red border and rounded bottom
], id="modal_new_lawyer", size="lg", is_open=False, 
style={
    'background-color': '#333333', 
    'border-radius': '10px', 
    'box-shadow': '0 8px 16px rgba(0,0,0,0.7)',  # Strong shadow
    'border': '2px solid #FF0000'  # Red border around modal
})


# ======= Callbacks ======== #
# Callback para adicionar novos advogados
@app.callback(
    Output('store_adv', 'data'),
    Output('div_erro2', 'children'),
    Output('div_erro2', 'style'),
    Input('save_button_novo_advogado', 'n_clicks'),
    State('store_adv', 'data'),
    State('adv_nome', 'value'),
    State('adv_oab', 'value'),
    State('adv_cpf', 'value')
)
def novo_adv(n, dataset, nome, oab, cpf):
    erro = []
    style = {}
    if n:
        if None in [nome, oab, cpf]:
            return dataset, ["Todos dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}
        
        df_adv = pd.DataFrame(dataset)

        if oab in df_adv['OAB'].values:
            return dataset, ["Número de OAB ja existe no sistema!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}
        elif cpf in df_adv['CPF'].values:
            return dataset, ["Número de CPF ja existe no sistema!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}
        elif nome in df_adv['Advogado'].values:
            return dataset, [f"Nome {nome} ja existe no sistema!"], {'margin-bottom': '15px', 'color': 'red', 'text-shadow': '2px 2px 8px #000000'}
        
        df_adv.loc[df_adv.shape[0]] = [nome, oab, cpf]
        dataset = df_adv.to_dict()
        return dataset, ["Cadastro realizado com sucesso!"], {'margin-bottom': '15px', 'color': 'green', 'text-shadow': '2px 2px 8px #000000'}
    return dataset, erro, style
