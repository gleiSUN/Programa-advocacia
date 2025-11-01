from logging import exception
import dash
import plotly.express as px
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from datetime import timedelta, date

import json
import pandas as pd

from app import app
from sql_beta import df_proc, df_adv

col_centered_style={'display': 'flex', 'justify-content': 'center'}

# ========= Layout ========= #
import dash_bootstrap_components as dbc
from datetime import date

# Assuming col_centered_style, df_adv, and other variables are defined elsewhere
# Add FontAwesome CSS link to ensure icons load (if not already in your app)
fontawesome_link = html.Link(href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css", rel="stylesheet")

layout = dbc.Modal([
    # Include FontAwesome link at the top to ensure icons appear
    fontawesome_link,
    
    dbc.ModalHeader(
        dbc.ModalTitle([
            html.I(className='fas fa-plus-circle', style={'margin-right': '10px', 'color': '#FF0000'}),  # Red plus-circle icon
            "Adicione Um Processo"
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
                # Empresa
                dbc.Label('Empresa', html_for='empresa_matriz', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dcc.Dropdown(id='empresa_matriz', clearable=False, className='dbc',
                    options=['Escritório Matriz', 'Filial Porto Alegre', 'Filial Curitiba', 'Filial Canoas'],
                    style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}),  # White dropdown with red border
                # Tipo de Processo
                dbc.Label('Tipo de Processo', html_for='tipo_processo', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dcc.Dropdown(id='tipo_processo', clearable=False, className='dbc',
                    options=['Civil', 'Criminal', 'Previdenciário', 'Trabalhista', 'Vara de Família'],
                    style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}),  # White dropdown with red border
                # Ação
                dbc.Label('Ação', html_for='acao', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dcc.Dropdown(id='acao', clearable=False, className='dbc',
                    options=['Alimentos', 'Busca e Apreensão', 'Cautelar Inominada', 'Consignação', 'Habeas Corpus', 'Mandado de Segurança', 'Reclamação'],
                    style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}),  # White dropdown with red border
            ], sm=12, md=4),
            dbc.Col([
                dbc.Label("Descrição", html_for='input_desc', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.Textarea(id="input_desc", placeholder="Escreva aqui observações sobre o processo...", 
                             style={'height': '80%', 'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}),  # White textarea with red border
            ], sm=12, md=8)
        ]),
        html.Hr(style={'border-color': '#FF0000', 'border-width': '2px'}),  # Red horizontal rule
        dbc.Row([
            dbc.Col([
                dbc.Label("Vara", html_for='vara', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.RadioItems(id='vara',
                    options=[{'label': 'Civil', 'value': 'Civil'},
                            {'label': 'Conciliação e Julgamento', 'value': 'Conciliação e Julgamento'},
                            {'label': 'Trabalhista', 'value': 'Trabalhista'},
                            {'label': 'Vara de Família', 'value': 'Vara de Família'}],
                    style={'color': '#FFFFFF'})  # White text for radio items
            ], sm=12, md=4),
            dbc.Col([
                dbc.Label("Fase", html_for='fase', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.RadioItems(id='fase', inline=True,
                    options=[{'label': 'Elaboração', 'value': 'Elaboração'},
                            {'label': 'Execução', 'value': 'Execução'},
                            {'label': 'Impugnação', 'value': 'Impugnação'},
                            {'label': 'Instrução', 'value': 'Instrução'},
                            {'label': 'Recurso', 'value': 'Recurso'},
                            {'label': 'Suspenso', 'value': 'Suspenso'}],
                    style={'color': '#FFFFFF'})  # White text for radio items
            ], sm=12, md=5),
            dbc.Col([
                dbc.Label("Instância", html_for='instancia', style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                dbc.RadioItems(id='instancia',
                    options=[{'label': '1A Instância', 'value': 1},
                            {'label': '2A Instância', 'value': 2}],
                    style={'color': '#FFFFFF'})  # White text for radio items
            ], sm=12, md=3)
        ]),
        html.Hr(style={'border-color': '#FF0000', 'border-width': '2px'}),  # Red horizontal rule
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data Inicial - Data Final", style={'color': '#FF0000', 'font-weight': 'bold'})  # Red label
                    ], style=col_centered_style),
                    dbc.Col([
                        dcc.DatePickerSingle(
                            id='data_inicial',
                            className='dbc',
                            min_date_allowed=date(1999, 12, 31),
                            max_date_allowed=date(2030, 12, 31),
                            initial_visible_month=date.today(),
                            date=date.today(),
                            style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}  # White date picker with red border
                        ),
                        dcc.DatePickerSingle(
                            id='data_final',
                            className='dbc',
                            min_date_allowed=date(1999, 12, 31),
                            max_date_allowed=date(2030, 12, 31),
                            initial_visible_month=date.today(),
                            date=None,
                            style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}  # White date picker with red border
                        ),
                    ], style=col_centered_style)
                ]),
                html.Br(),
                dbc.Switch(id='processo_concluido', label="Processo Concluído", value=False, 
                           style={'color': '#FFFFFF'}),  # White label for switch
                dbc.Switch(id='processo_vencido', label="Processo Vencido", value=False, 
                           style={'color': '#FFFFFF'}),  # White label for switch
                html.P("O filtro de data final só será computado se o checklist estiver marcado.", className='dbc', 
                       style={'font-size': '80%', 'color': '#FFFFFF'}),  # White text for note
            ], sm=12, md=5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Selecione o advogado responsável: ", style={'color': '#FF0000', 'font-weight': 'bold'}),  # Red label
                        dcc.Dropdown(
                            id='advogados_envolvidos',
                            options=[{'label': i, 'value': i} for i in df_adv['Advogado']],
                            className='dbc',
                            style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'}  # White dropdown with red border
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Input(id="input_cliente", placeholder="Nome completo do cliente...", type="text", 
                                  style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White input with red border
                    ])
                ], style={'margin-top': '15px', 'padding': '15px'}),
                dbc.Row([
                    dbc.Col([
                        dbc.Input(id="input_cliente_cpf", placeholder="CPF do cliente (apenas números)...", type="number", 
                                  style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White input with red border
                    ])
                ], style={'padding': '15px'}),
            ], sm=12, md=7)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='input_local_arquivo', clearable=False, className='dbc', placeholder="Local de Arquivo/Local Físico",
                    options=['Armário Principal', 'Armário 17 gaveta 2', 'Armário 5 gaveta 1', 'Arquivo 01', 'Arquivo 02'],
                    style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White dropdown with red border
            ], sm=12, md=5, style={'padding': '15px'}),
            dbc.Col([
                dbc.Input(id="input_no_processo", placeholder="Insira o número do Processo", type="number", disabled=False, 
                          style={'background-color': '#FFFFFF', 'color': '#000000', 'border-color': '#FF0000'})  # White input with red border
            ], sm=12, md=7, style={'padding': '15px'})
        ], style={'margin-top': '15px'}),
        html.H5(id='div_erro', style={'color': '#FF0000', 'text-align': 'center', 'margin-top': '20px'})  # Red error message, centered
    ], style={'background-color': '#333333', 'color': '#FFFFFF', 'padding': '20px'}),  # Gray body with padding
    dbc.ModalFooter([
        dbc.Button([
            html.I(className='fas fa-times', style={'margin-right': '8px', 'color': '#FFFFFF'}),  # White close icon
            "Cancelar"
        ], id="cancel_button_novo_processo", 
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
        ], id="save_button_novo_processo", 
        style={
            'background-color': '#333333', 
            'border-color': '#FF0000', 
            'color': '#FFFFFF',
            'border-radius': '5px',
            'font-weight': 'bold'
        },  # Gray button with red border
        color="success")
    ], style={'background-color': '#333333', 'border-top': '3px solid #FF0000', 'border-radius': '0 0 10px 10px'})  # Gray footer with red border and rounded bottom
], id="modal_processo", size="lg", is_open=False, 
style={
    'background-color': '#333333', 
    'border-radius': '10px', 
    'box-shadow': '0 8px 16px rgba(0,0,0,0.7)',  # Strong shadow
    'border': '2px solid #FF0000'  # Red border around modal
})

# Callback para teste de abrir o modal
@app.callback(
    Output('modal_processo', 'is_open'),
    Output('store_intermedio', 'data'),
    Input({'type': 'editar_processo', 'index': ALL}, 'n_clicks'),
    Input('processo_button', 'n_clicks'),
    Input("cancel_button_novo_processo", 'n_clicks'),
    State('modal_processo', 'is_open'),
    State('store_proc', 'data'),
    State('store_intermedio', 'data')
)
def abrir_modal_processo(n_editar, n_new, n_cancel, is_open, store_proc, store_intermedio):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    first_call = True if callback_context.triggered[0]['value'] == None else False
    if first_call:
        return is_open, store_intermedio

    if (trigg_id == 'processo_button') or (trigg_id == 'cancel_button_novo_processo'):
        df_int = pd.DataFrame(store_intermedio)
        df_int = df_int[:-1]
        store_intermedio = df_int.to_dict()

        return not is_open, store_intermedio

    if n_editar:
        trigg_dict = json.loads(callback_context.triggered[0]['prop_id'].split('.')[0])
        numero_processo = trigg_dict['index']

        df_int = pd.DataFrame(store_intermedio)
        df_proc = pd.DataFrame(store_proc)

        valores = df_proc.loc[df_proc['No Processo'] == numero_processo].values.tolist()
        valores = valores[0] + [True]

        df_int = df_int[:-1]
        df_int.loc[len(df_int)] = valores
        store_intermedio = df_int.to_dict()

        return not is_open, store_intermedio

# Callback para CRUD de processos
@app.callback(
    Output('store_proc', 'data'),
    Output('div_erro', 'children'),
    Output('div_erro', 'style'),
    Output('input_no_processo', 'value'),
    Output('empresa_matriz', 'value'),
    Output('tipo_processo', 'value'),
    Output('acao', 'value'),
    Output('vara', 'value'),
    Output('fase', 'value'),
    Output('instancia', 'value'),
    Output('data_inicial', 'date'),
    Output('data_final', 'date'),
    Output('processo_concluido', 'value'),
    Output('processo_vencido', 'value'),
    Output('advogados_envolvidos', 'value'),
    Output('input_cliente', 'value'),
    Output('input_cliente_cpf', 'value'),
    Output('input_desc', 'value'),
    Output('input_no_processo', 'disabled'),
    Input('processo_button', 'n_clicks'),
    Input('save_button_novo_processo', 'n_clicks'),
    Input({'type': 'deletar_processo', 'index': ALL}, 'n_clicks'),
    Input('store_intermedio', 'data'),
    State('modal_processo', 'is_open'),
    State('store_proc', 'data'),
    State('input_no_processo', 'value'),
    State('empresa_matriz', 'value'),
    State('tipo_processo', 'value'),
    State('acao', 'value'),
    State('vara', 'value'),
    State('fase', 'value'),
    State('instancia', 'value'),
    State('data_inicial', 'date'),
    State('data_final', 'date'),
    State('processo_concluido', 'value'),
    State('processo_vencido', 'value'),
    State('advogados_envolvidos', 'value'),
    State('input_cliente', 'value'),
    State('input_cliente_cpf', 'value'),
    State('input_desc', 'value'),
    prevent_initial_call=True
)
def crud_processos(n_new, n_save, n_delete, store_int, is_open, store_proc, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc):
    first_call = True if (callback_context.triggered[0]['value'] == None or callback_context.triggered[0]['value'] == False) else False
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if first_call:
        no_processo = empresa = tipo = acao = vara = fase = instancia = data_inicial = data_final = advogados = cliente = cpf_cliente = desc = None
        processo_concluido = processo_vencido = False
        return store_proc, [], {}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False

    if trigg_id == 'save_button_novo_processo':
        df_proc = pd.DataFrame(store_proc)
        df_int = pd.DataFrame(store_int)
        
        if len(df_int.index) == 0: # Novo processo
            if None in [no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, advogados, cliente, cpf_cliente]:
                return store_proc, ["Todos dados são obrigatórios para registro!"], {'margin-bottom': '15px', 'color': 'red'}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False
            if (no_processo in df_proc['No Processo'].values):
                return store_proc, ["Número de processo ja existe no sistema!"], {'margin-bottom': '15px', 'color': 'red'}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False
            
            data_inicial = pd.to_datetime(data_inicial).date()
            try:
                data_final = pd.to_datetime(data_final).date()
            except:
                pass
                
            df_proc.reset_index(drop=True, inplace=True)
            
            processo_concluido = 0 if processo_concluido == False else 1
            processo_vencido = 0 if processo_vencido == False else 1
            if processo_concluido == 0: data_final = None

            df_proc.loc[df_proc.shape[0]] = [no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final,
                                            processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc]
            
            store_proc = df_proc.to_dict()
            no_processo = empresa = tipo = acao = vara = fase = instancia = data_inicial = data_final = advogados = cliente = cpf_cliente = desc = None
            processo_concluido = processo_vencido = False
            return store_proc, ['Processo salvo com sucesso!'], {'margin-bottom': '15px', 'color': 'green'}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False

        else:   # Edição de processo
            processo_concluido = 0 if processo_concluido == False else 1
            processo_vencido = 0 if processo_vencido == False else 1
            if processo_concluido == 0: data_final = None

            index = df_proc.loc[df_proc['No Processo'] == no_processo].index[0]
            df_proc.loc[index, df_proc.columns] = [no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc]
            
            store_proc = df_proc.to_dict()
            no_processo = empresa = tipo = acao = vara = fase = instancia = data_inicial = data_final = advogados = cliente = cpf_cliente = desc = None
            processo_concluido = processo_vencido = False
            
            return store_proc, ['Processo salvo com sucesso!'], {'margin-bottom': '15px', 'color': 'green'}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False

    if 'deletar_processo' in trigg_id:
        df_proc = pd.DataFrame(store_proc)

        trigg_id_dict = json.loads(trigg_id)
        numero_processo = trigg_id_dict['index']

        index_processo = df_proc.loc[df_proc['No Processo'] == numero_processo].index[0]
        df_proc.drop(index_processo, inplace=True)
        df_proc.reset_index(drop=True, inplace=True)

        store_proc = df_proc.to_dict()
        no_processo = empresa = tipo = acao = vara = fase = instancia = data_inicial = data_final = advogados = cliente = cpf_cliente = desc = None
        processo_concluido = processo_vencido = False
        return store_proc, [], {}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False

    if (trigg_id == 'store_intermedio') and is_open:
        try:
            df = pd.DataFrame(callback_context.triggered[0]['value'])
            df_proc = pd.DataFrame(store_proc)
            valores = df.head(1).values.tolist()[0]

            no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, disabled = valores

            processo_concluido = False if processo_concluido == 0 else True
            processo_vencido = False if processo_vencido == 0 else True

            return store_proc, ['Modo de Edição: Número de Processo não pode ser alterado'], {'margin-bottom': '15px', 'color': 'green'}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, disabled
        except:
            no_processo = empresa = tipo = acao = vara = fase = instancia = data_inicial = data_final = advogados = cliente = cpf_cliente = desc = None
            processo_concluido = processo_vencido = False
            return store_proc, [], {}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False

    no_processo = empresa = tipo = acao = vara = fase = instancia = data_inicial = data_final = advogados = cliente = cpf_cliente = desc = None
    processo_concluido = processo_vencido = False
    return store_proc, [], {}, no_processo, empresa, tipo, acao, vara, fase, instancia, data_inicial, data_final, processo_concluido, processo_vencido, advogados, cliente, cpf_cliente, desc, False

# Callback pra atualizar o dropdown de advogados
@app.callback(
    Output('advogados_envolvidos', 'options'),
    Input('store_adv', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['Advogado']]
