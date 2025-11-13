import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
import hashlib
from functools import wraps

# import from folders
from app import *
from components import home, sidebar
from sql_beta import df_proc, df_adv

# ========= SISTEMA DE AUTENTICAÇÃO ========= #
# Criar tabela de usuários no banco
def criar_tabela_usuarios():
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nome TEXT NOT NULL,
            nivel_acesso TEXT DEFAULT 'user'
        )
    ''')
    
    # Inserir usuário admin padrão se não existir
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, nome, nivel_acesso) VALUES (?, ?, ?, ?)",
            ("admin", senha_hash, "Administrador", "admin")
        )
        conn.commit()
    conn.close()

# Verificar credenciais
def verificar_login(username, password):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        return {
            'id': usuario[0],
            'username': usuario[1],
            'nome': usuario[3],
            'nivel_acesso': usuario[4]
        }
    return None

# Decorator para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado'):
            return dcc.Location(pathname='/login', id='redirect-login')
        return f(*args, **kwargs)
    return decorated_function

# ========= LAYOUT DA TELA DE LOGIN ========= #
def criar_layout_login():
    return dbc.Container([
        dcc.Location(id='url-login', refresh=True),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H2([
                            html.I(className="fas fa-gavel", style={'margin-right': '10px', 'color': '#FF0000'}),
                            "LEXManager - Login"
                        ], className="text-center", style={'color': '#FF0000'})
                    ], style={'background-color': '#333333', 'border-bottom': '2px solid #FF0000'}),
                    
                    dbc.CardBody([
                        dbc.Form([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Usuário:", style={'color': '#FFFFFF', 'font-weight': 'bold'}),
                                    dbc.Input(
                                        id="login-username",
                                        type="text",
                                        placeholder="Digite seu usuário",
                                        style={'background-color': '#FFFFFF', 'color': '#000000', 'border': '1px solid #FF0000'}
                                    ),
                                ], className="mb-3")
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Senha:", style={'color': '#FFFFFF', 'font-weight': 'bold'}),
                                    dbc.Input(
                                        id="login-password",
                                        type="password",
                                        placeholder="Digite sua senha",
                                        style={'background-color': '#FFFFFF', 'color': '#000000', 'border': '1px solid #FF0000'}
                                    ),
                                ], className="mb-3")
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button(
                                        "Entrar",
                                        id="login-button",
                                        color="danger",
                                        className="w-100",
                                        style={'background-color': '#FF0000', 'border': 'none', 'font-weight': 'bold'}
                                    ),
                                ], className="mb-3")
                            ]),
                            
                            html.Hr(style={'border-color': '#FF0000'}),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.Small(
                                        
                                        className="text-center d-block",
                                        style={'color': '#CCCCCC'}
                                    )
                                ])
                            ])
                        ])
                    ], style={'background-color': '#333333', 'padding': '30px'})
                ], style={
                    'max-width': '400px',
                    'margin': '100px auto',
                    'border': '2px solid #FF0000',
                    'border-radius': '10px',
                    'box-shadow': '0 4px 8px rgba(255,0,0,0.3)'
                })
            ], md=6, lg=4, className="mx-auto")
        ], className="align-items-center justify-content-center", style={'height': '100vh'})
    ], fluid=True, style={'background-color': '#1a1a1a', 'height': '100vh'})

# ========= MODIFICAÇÃO DO LAYOUT PRINCIPAL ========= #
# Criar estrutura para Store intermediária
data_int = {
    'No Processo': [], 
    'Empresa': [],
    'Tipo': [],
    'Ação': [],
    'Vara': [],
    'Fase': [],
    'Instância': [],
    'Data Inicial': [],
    'Data Final': [],
    'Processo Concluído': [],
    'Processo Vencido': [],
    'Advogados': [],
    'Cliente': [],
    'Cpf Cliente': [],
    'Descrição': [],
    'disabled': []
}

store_int = pd.DataFrame(data_int)

# Session para armazenar dados de login
session = {'usuario_logado': None}

app.layout = dbc.Container(children=[
    dcc.Location(id="url"),
    dcc.Store(id='store_intermedio', data=store_int.to_dict()),
    dcc.Store(id='store_adv', data=df_adv.to_dict(), storage_type='session'),
    dcc.Store(id='store_proc', data=df_proc.to_dict()),
    dcc.Store(id='session-store', data=session, storage_type='session'),
    html.Div(id='div_fantasma', children=[]),
    html.Div(id="page-content")
], fluid=True, style={'padding': '0px'})

# ========= CALLBACKS DE AUTENTICAÇÃO ========= #
@app.callback(
    Output('page-content', 'children'),
    Output('session-store', 'data'),
    Input('url', 'pathname'),
    State('session-store', 'data')
)
def render_page_content(pathname, session_data):
    # Verificar se usuário está logado
    usuario_logado = session_data.get('usuario_logado') if session_data else None
    
    if not usuario_logado and pathname != '/login':
        return criar_layout_login(), session_data
    
    if pathname == '/login' and usuario_logado:
        return dcc.Location(pathname='/home', id='redirect-home'), session_data
        
    if pathname == '/login':
        return criar_layout_login(), session_data
    
    # Usuário logado - renderizar aplicação normal
    if usuario_logado and (pathname == '/home' or pathname == '/'):
        return dbc.Row([
            dbc.Col([sidebar.layout], md=2, style={'padding': '0px'}),
            dbc.Col([
                dbc.Container(id="main-content", children=home.layout, fluid=True, 
                            style={'height': '100%', 'width': '100%', 'padding-left': '14px'})
            ], md=10, style={'padding': '0px'}),
        ]), session_data
    
    # Página não encontrada
    return dbc.Container([
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"O caminho '{pathname}' não foi reconhecido..."),
        dbc.Button("Voltar ao Início", href="/home", color="danger")
    ]), session_data

@app.callback(
    Output('url', 'pathname'),
    Output('session-store', 'data', allow_duplicate=True),
    Input('login-button', 'n_clicks'),
    State('login-username', 'value'),
    State('login-password', 'value'),
    State('session-store', 'data'),
    prevent_initial_call=True
)
def fazer_login(n_clicks, username, password, session_data):
    if n_clicks:
        if not username or not password:
            return '/login', session_data
        
        usuario = verificar_login(username, password)
        if usuario:
            session_data['usuario_logado'] = usuario
            return '/home', session_data
    
    return '/login', session_data

# Callback para logout (adicionar no sidebar.py)
@app.callback(
    Output('session-store', 'data', allow_duplicate=True),
    Output('url', 'pathname', allow_duplicate=True),
    Input('logout-button', 'n_clicks'),
    State('session-store', 'data'),
    prevent_initial_call=True
)
def fazer_logout(n_clicks, session_data):
    if n_clicks:
        session_data['usuario_logado'] = None
        return session_data, '/login'
    return session_data, dash.no_update

# Dcc.Store back to file (mantido original)
@app.callback(
    Output('div_fantasma', 'children'),
    Input('store_adv', 'data'),
    Input('store_proc', 'data'),
)
def update_file(adv_data, proc_data):
    df_adv_aux = pd.DataFrame(adv_data)
    df_proc_aux = pd.DataFrame(proc_data)

    conn = sqlite3.connect('sistema.db')
    df_proc_aux.to_sql('processos', conn, if_exists='replace', index=False)
    df_adv_aux.to_sql('advogados', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    return []

if __name__ == '__main__':
    criar_tabela_usuarios()  # Criar tabela de usuários ao iniciar
    app.run(debug=True)