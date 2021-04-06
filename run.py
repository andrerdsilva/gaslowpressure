import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
from flask import Flask
import os

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app.config.supress_callback_exceptions = True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server = server, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    
    #html.H1(children='Dimensionamento de redes de gás de baixa pressão'),
    html.H1('Dimensionamento de redes de gás de baixa pressão até 7,5 kPa'),
    html.Label('Selecione os aparelhos de gás:'),
    dcc.Dropdown(
        id='aparelhos',
        options=[
            {'label': '1 x Fogão 4 bocas sem forno', 'value': 6966},
            {'label': '2 x Fogão 4 bocas sem forno', 'value': 2*6966},
            {'label': '1 x Fogão 4 bocas com forno', 'value': 9288},
            {'label': '2 x Fogão 4 bocas com forno', 'value': 2*9288},
            {'label': '1 x Fogão 6 bocas sem forno', 'value': 9976},
            {'label': '2 x Fogão 6 bocas sem forno', 'value': 2*9976},
            {'label': '1 x Fogão 6 bocas com forno', 'value': 13390},
            {'label': '2 x Fogão 6 bocas com forno', 'value': 2*13390},
            {'label': '1 x Aquecedor de passagem 15 L/min', 'value': 22000},
            {'label': '1 x Aquecedor de passagem 18 L/min', 'value': 26500},
            {'label': '1 x Aquecedor de passagem 25 L/min', 'value': 36000},
            {'label': '1 x Aquecedor de passagem 30 L/min', 'value': 45500},
            {'label': '1 x Aquecedor de passagem 35 L/min', 'value': 49000},
            {'label': '1 x Aquecedor de passagem 42 L/min', 'value': 59856},
            {'label': '2 x Aquecedor de passagem 15 L/min', 'value': 2*22000},
            {'label': '2 x Aquecedor de passagem 18 L/min', 'value': 2*26500},
            {'label': '2 x Aquecedor de passagem 25 L/min', 'value': 2*36000},
            {'label': '2 x Aquecedor de passagem 30 L/min', 'value': 2*45500},
            {'label': '2 x Aquecedor de passagem 35 L/min', 'value': 2*45500},
            {'label': '2 x Aquecedor de passagem 42 L/min', 'value': 2*59856}
        ],
        value=[13390],
        multi=True
    ),
    
    html.Div([
        html.Div([
            html.Label('Material do tubo:'),
            dcc.Dropdown(
                id='material',
                options=[
                    {'label': 'PEX', 'value': 'PEX' },
                    {'label': 'Cobre Classe A', 'value': 'Cobre Classe A'}
                ],
                value='PEX',
                multi=False
            )],style={'width': '18%',
                      'float': 'left',
                      'margin-right': '18px'}),
        
        html.Div([  
            html.Label('Tipo de gás:'),
            dcc.RadioItems(
            id='tipogas',
            options=[
                {'label': 'GLP', 'value': 'GLP'},
                {'label': 'GN', 'value': 'GN'}
            ],
            value='GN'
            )],style={'width': '18%',
                      'float': 'left'}),
        html.Div([
            html.Label('Fator de potência:'),
            dcc.RadioItems(
            id='FP',
            options=[
                {'label': 'Sim', 'value': 'True'},
                {'label': 'Não', 'value': 'False'}
            ],
            value='False'
            )],style={'width': '18%',
                      'float': 'left'}),
        
        html.Div([
            html.Label('Pressão relativa inicial do GN (kPa):'),
            dcc.Input(
            id='PRGN',
            placeholder='2.2',
            type='number',
            value=2.2
            )],style={'width': '20%',
                      'float': 'left'}),

        html.Div([
            html.Label('Pressão relativa inicial do GLP (kPa):'),
            dcc.Input(
            id='PRGLP',
            placeholder='2.8',
            type='number',
            value=2.8

            )],style={
                      'float': 'right'
                      })
               ], style={ 'margin-bottom': '90px'}),

    #html.Div(id='dd-output-container')
    dcc.Graph(
        id='perda-carga'
    ),

    dcc.Graph(
        id='velocidade'
    )
    
    
])


#@app.callback(
#    dash.dependencies.Output('dd-output-container', 'children'),
#    [dash.dependencies.Input('aparelho', 'value')])


@app.callback(
    dash.dependencies.Output('perda-carga', 'figure'),
    [dash.dependencies.Input('aparelhos', 'value')],
    [dash.dependencies.Input('material', 'value')],
    #[dash.dependencies.Input('comprimento', 'value')],
    [dash.dependencies.Input('tipogas', 'value')],
    [dash.dependencies.Input('FP', 'value')],
    [dash.dependencies.Input('PRGN', 'value')],
    [dash.dependencies.Input('PRGLP', 'value')]
    #[dash.dependencies.Input('asc', 'value')],
    #[dash.dependencies.Input('des', 'value')],
    )


#def update_output(aparelhos):
#    return(sum(aparelhos))

def perda_carga(aparelhos,material,tipogas,FP,PRGN,PRGLP):
    potencia = sum(aparelhos)

    if(FP=='True'):
        if(potencia<21000):
            potencia = potencia
        elif( potencia>= 21000 and potencia < 576520):
            potencia = potencia * 1/(1+0.001*(potencia/60-349)**0.8712)
        elif(potencia>= 576520 and potencia < 1200000):
            potencia = potencia * 1/(1+0.4705*(potencia/60-1055)**0.19931)
        else:
            potencia = potencia * 23/100
    else:
        potencia = potencia



    if(material=='PEX'):       
        DN = [16,20,26,32]
        DI = [12,16,20,26]
    elif(material=='Cobre Classe A'):
        DN = [15,22,28,35,42,54,66,79,104]
        DI = [13.4, 20.2, 26.2, 32.8, 39.8, 51.6, 64.3, 76.4, 101.8]
    else:
        DN = []
        DI = []

            
    if(tipogas=='GN'):
        Q = potencia/8600

        fig = go.Figure()
        x = np.arange(25)
        for i in range(0,len(DN)):
            fig.add_trace(go.Scatter(x=x, y=  ( (206580*(Q**1.8)*(0.6)**0.8 * x)/ (DI[i])**4.8)/(100 * PRGN ) *100,
                    mode='lines',
                    name= 'DN ' + str(DN[i])))
        fig.add_trace(go.Scatter(x=x,y=10+0*x,
                mode='lines',
                name='10% da pressão de operação',
                line = dict(color='black', width=4, dash='dash')))

        fig.update_xaxes(title_text='Comprimento equivalente (m)',
                         dtick=1.0,
                         range=[0, 20])
        fig.update_yaxes(title_text='Perda de carga (%)',
                         range=[0, 15])

        return(fig)

    if(tipogas=='GLP'):
        Q = potencia/24000

        fig = go.Figure()
        x = np.arange(25)
        for i in range(0,len(DN)):
            fig.add_trace(go.Scatter(x=x, y= ( (2273*1.8*x*Q**1.82)/ ( DI[i]**4.82) )/PRGLP * 100,
                    mode='lines',
                    name= 'DN ' + str(DN[i])))
        fig.add_trace(go.Scatter(x=x,y=10+0*x,
                mode='lines',
                name='10% da pressão de operação',
                line = dict(color='black', width=4, dash='dash')))

        fig.update_xaxes(title_text='Comprimento equivalente (m)',
                         dtick=1.0,
                         range=[0, 20])
        fig.update_yaxes(title_text='Perda de carga (%)',
                         range=[0, 15])

        return(fig)



@app.callback(
    dash.dependencies.Output('velocidade', 'figure'),
    [dash.dependencies.Input('aparelhos', 'value')],
    [dash.dependencies.Input('material', 'value')],
    [dash.dependencies.Input('tipogas', 'value')],
    [dash.dependencies.Input('FP', 'value')],
    [dash.dependencies.Input('PRGN', 'value')],
    [dash.dependencies.Input('PRGLP', 'value')]
    )

def velocidade(aparelhos,material,tipogas,FP,PRGN,PRGLP):
    potencia = sum(aparelhos)

    if(FP=='True'):
        if(potencia<21000):
            potencia = potencia
        elif( potencia>= 21000 and potencia < 576520):
            potencia = potencia * 1/(1+0.001*(potencia/60-349)**0.8712)
        elif(potencia>= 576520 and potencia < 1200000):
            potencia = potencia * 1/(1+0.4705*(potencia/60-1055)**0.19931)
        else:
            potencia = potencia * 23/100
    else:
        potencia = 1*potencia


    if(material=='PEX'):       
        DN = [16,20,26,32]
        DI = [12,16,20,26]
    elif(material=='Cobre Classe A'):
        DN = [15,22,28,35,42,54,66,79,104]
        DI = [13.4, 20.2, 26.2, 32.8, 39.8, 51.6, 64.3, 76.4, 101.8]
    else:
        DN = []
        DI = []

            
    if(tipogas=='GN'):
        Q = potencia/8600


        fig = go.Figure()
        x = np.arange(110)

        fig.add_trace(go.Scatter( x=x, y= 354 *Q/((PRGN*0.010197 + 1.033) *x**2 ) ,
                 mode='lines',
                 name= 'Velocidade'  ))

        fig.add_trace(go.Scatter(x=x,y=20+0*x,
                mode='lines',
                name='Velocidade máxima = 20 m/s',
                line = dict(color='black', width=4, dash='dash')))

        y = []
        for i in range(0,len(DN)):
            y.append(354 *Q/((PRGN*0.010197 + 1.033) *DI[i]**2))

        DN2 = []
        for i in range(0,len(DN)):
            DN2.append('DN ' + str(DN[i]))
            
        fig.add_trace(go.Scatter(x=DI,y=y,
                mode='markers',
                name= material,
                text=DN2,
                line = dict(color='red', width=4)
                ))
        

        fig.update_xaxes(title_text='Diâmetro interno (mm)',
                         )

        fig.update_yaxes(title_text='Velocidade (m/s)',
                         range=[0,25]
                         )

        return(fig)



    if(tipogas=='GLP'):
        Q = potencia/24000


        fig = go.Figure()
        x = np.arange(110)

        fig.add_trace(go.Scatter( x=x, y= 354 *Q/((PRGLP*0.010197 + 1.033) *x**2 ) ,
                 mode='lines',
                 name= 'Velocidade'  ))

        fig.add_trace(go.Scatter(x=x,y=20+0*x,
                mode='lines',
                name='Velocidade máxima = 20 m/s',
                line = dict(color='black', width=4, dash='dash')))

        y = []
        for i in range(0,len(DN)):
            y.append(354 *Q/((PRGLP*0.010197 + 1.033) *DI[i]**2))

        DN2 = []
        for i in range(0,len(DN)):
            DN2.append('DN ' + str(DN[i]))
            
        fig.add_trace(go.Scatter(x=DI,y=y,
                mode='markers',
                name= material,
                text=DN2,
                line = dict(color='red', width=4)
                ))
        

        fig.update_xaxes(title_text='Diâmetro interno (mm)',
                         )

        fig.update_yaxes(title_text='Velocidade (m/s)',
                         range=[0,25]
                         )

        return(fig)


