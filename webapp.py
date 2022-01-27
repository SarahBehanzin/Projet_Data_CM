
#Importations utiles pour le traitement des données
from dash.html.Title import Title
import folium
import urllib.parse
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Importations utiles pour le dashboard
import plotly_express as px
import dash
from dash import dash_table
from plotly.subplots import make_subplots
from dash import dcc
from dash import html
from flask import Flask

#PERMET D'ÉVITER DE RECEVOIR UN WARNING DÛ AU FAIT QUE NOUS MODIFIONS LES VALEURS DE LA DATAFRAME
pd.options.mode.chained_assignment = None


app = dash.Dash(__name__)#création du dashboard


 #AJOUT DE L HISTOGRAMME DES COTES MAX DE VICTOIRES À DOMICILE DE BETBRAIN

app.layout = html.Div(children=[  

        html.H1(children='DASHBOARD 1', style={'textAlign': 'center'}),#titre général du dashboard

        dcc.Tabs(style={'borderTop':'3px solid #212121', 'borderRadius':'6px', 'boxShadow':'2px 2px 30px #a4b0be'}, colors={'background':'#dfe4ea'}, id="tabs", children=[   #création des différents "onglets"

            dcc.Tab(label="Présentation", children=[   #premier onglet
                html.Div(children=[
                    html.H1(children='Présentation du projet', style={'textAlign' :'center','background-color':'#dfe4ea'}),#titre de la page
                    dcc.Textarea(
                        id='présentation',
                        title='Présentation du dashboard',
                        value='Bienvenue!\n\nNous sommes Sarah Behanzin, Amine Belgacem et Shayan Arnal.\n On étudie ici les statistiques des différentes coupes de monde de football',
                        style={'fontFamily':'Arial','width':'100%', 'height':'1000', 'textAlign':'left', 'background-color':'#dfe4ea', 'font-size':'medium', 'font-style':'normal', 'resize':'none', 'border':'none'},
                        readOnly='readOnly',
                        draggable='false',
                        rows='20'
                    ),

                    html.H1(children='Données 2', style={'textAlign':'left'}),#première dataframe
                    dash_table.DataTable( #affichage de la base de donnée 
                        data=data.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in data.columns],
                        page_action='none',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'}
                    ),

                    html.H1(children='Données 3', style={'textAlign':'left'}),#deuxième dataframe
                    dash_table.DataTable(#affichage de la base de donnée 
                        data=data_stade.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in data_stade.columns],
                        page_action='none',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'}
                    )
                ])
            ]),


            dcc.Tab(label="Partie deux", children=[   #deuxième onglet
                html.Div(children=[
                    html.H1(children='Partie 2', style={'textAlign' :'center', 'background-color':'#dfe4ea'}),#titre de la page
                        dcc.Textarea(
                        id='histo',
                        title='Histogrammes',
                        value='Cliquer pour selectionner les données.',
                        style={'fontFamily':'Arial','width':'100%', 'height':'1000', 'textAlign':'left', 'background-color':'#dfe4ea', 'font-size':'medium', 'font-style':'normal', 'resize':'none','border':'none'},
                        readOnly='readOnly',
                        draggable='false',
                        rows='1'
                    ),

                        dcc.Graph(#affichage du premier graph
                            id='graph1',
                            figure=hist1,
                            style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px'}
                        ),

                        dcc.Graph(#affichage de deuxième graph
                            id='graph2',
                            figure=hist2,
                            style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px'}
                        ),
                        dcc.Graph(#affichage du troisième graph
                            id='graph3',
                            figure=hist3,
                            style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px'}
                        ),
                        dcc.Graph(#affichage du quatrième graph
                            id='graph4',
                            figure=hist4,
                            style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px'}
                        )
                ]),
            ]),



            dcc.Tab(label="Partie Trois", children=[   #quatrième onglet

                html.Div(children=[
                    html.H1(children='Cartes', style={'textAlign' :'center', 'background-color':'#dfe4ea'}),#titre de la page
                    html.H1(children='Partie 3', style={'textAlign':'left'}),#titre de la première carte
                    html.Iframe(#affichage de la première map
                        id='map1',
                        srcDoc=open('map_teams.html','r').read(),
                        width='60%',
                        height='600',
                        style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px', 'margin':'25'}
                    ),
                    html.H1(children='Demo', style={'textAlign':'left'}),#titre de la deuxième carte
                    html.Iframe(#affichage de la deuxième map
                        id='map2',
                        srcDoc=open('map_matchs.html','r').read(),
                        width='60%',
                        height='600',
                        style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px','margin':'25'}
                    )
                ])
            ])    
        ])
    ])

    app.run_server(debug=True)

    return None

if __name__ == '__main__':
    main()


                    

