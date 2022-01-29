'''
authors:
    sarah.behanzin@edu.esiee.fr
    mohammad-amine.belgacem@edu.esiee.fr
    shayan.arnal@edu.esiee.fr
'''
#Importations utiles pour le traitement des données
import urllib.request
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt

#Importations utiles pour le dashboard
import plotly_express as px
import dash
import base64

from dash import dcc
from dash import html
from dash import dash_table
import imageio  

from cgi import test
from cgitb import text
from cmath import nan
from os import name
import string
from numpy import NaN
import pandas as pd
import requests
import string
import pymongo
import matplotlib.pyplot as plt
from googletrans import Translator
from bs4 import BeautifulSoup
pd.options.mode.chained_assignment = None  # default='warn' //permet de supprimmer un avertissement

translator=Translator() #fonction transmlator

#Base de données contenant la liste des pays conforme à la norme ISO 3166-1

df_pays=pd.read_csv("sql-pays.csv", names=["id ", "alpha2", "alpha3", "nom_français", "nom_anglais"]) #on lit les données et on rajoute le header car il n'était pas dans le fichier


#FONCTIONS

def fonction_correspondance(document):
    '''
    Permet de transformer la valeur de la case d'une dataframe
    
    Args:
        document:nom de la dataframe
    
    Returns:
        None

    '''
    for i in range(len(document)):
        if document[i]=="USA":
            document[i]="États-Unis"
        if document[i]=="RP Chine":
            document[i]="Chine"
        if document[i]=="Angleterre" or document[i]=="England":
            document[i]="Royaume-Uni"
        if document[i]=="République Fédérale d'Allemagne":
            document[i]="Allemagne"
        if document[i]=="Union soviétique":
            document[i]="Fédération de Russie"
        if document[i]=="Tchécoslovaquie":
            document[i]="République Tchèque"
    return None


def fonction_pays(nom_pays):
    '''
    Retourne le code du pays

    Args:
        nom_pays:nom original du pays

    Returns: code du pays
    '''
    nom_final=[]
    for i in range(1,len(df_pays)):
        if df_pays['nom_français'][i]==nom_pays:
            nom_final=df_pays['alpha3'][i]
    return nom_final

def traduction(document):
    '''
    Traduie un mot présent dans la colonne une dataframe à partir de la dataframe des pays

    Args:
        document: dataframe que l'on veut traduire
    
    Returns:
        None
    '''
    for mot in range(len(document)):
        for i in range(1,len(df_pays)):#on parcourt le dataframe des pays
            if df_pays['nom_anglais'][i]==document[mot]:#si le nom anglais fait partie est égal au nom du document
                document[mot]=str(df_pays['nom_français'][i])#on remplace par le nom français
    return None

def cursor_to_liste(cursor):
    '''
    Retourne deux listes contenant des valeurs contenues dans un curseur mongo

    Args:
        cursor:curseur mongo
    
    Returns: les deux listes obtenues après avoir parcouru les dictionnaires contenus dans la liste
    '''
    x=[]
    y=[]
    liste=list(cursor)#on met le curseur sous forme de liste
    for i in range(len(liste)): #on parcourt la liste
        x.append(list(liste[i].values())[0]) #dans la liste x, on ajoute la première partie des valeurs du dictionnaire
        y.append(list(liste[i].values())[1]) #dans la liste y, on ajoute la seconde partie des valeurs du dictionnaire
    return x,y #on retourne les deux listes

def split_columns(col,new_col):
    '''
    Retourne deux colonnes en fonction de la valeur d'une

    Args:
        col: colonne de base
        new_col: nouvellle colonne
        
    Returns: les valeurs des deux colonnes
    '''
    for i in range(len(col)):#on parcourt la colonne de base
        taille=len(col[i].split(' '))#taille correspond à la taille de la colonne une fois coupée en fonction des espaces
        new_col[i]=new_col[i].split(' ')[taille-1]#la nouvelle colonne contient le dernier élément de la colonne de base coupée
        col[i]=col[i].split(new_col[i])[0] #la colonne de base ne garde que le reste
    return new_col,col #on retourne les deux colonnes
        

def main():

#------------------------------------------------------------------------------------------------------------------------------------------------#

    #METTRE LES DONNÉES SOUS FORME DE DATAFRAME
    df_CM_masculin=pd.read_csv('pays.csv')#on lit les données stockées dans le bon fichier csv
    df_CM_feminin=pd.read_csv('pays_f.csv')#on lit les données stockées dans le bon fichier csv

    #ici on a ajouté un encodage pour pouvoir lire les caractères spéciaux
    df_coord=pd.read_csv('coord.csv',encoding="ISO-8859-1")
    df_but_fem=pd.read_csv('but_f.csv',encoding="ISO-8859-1")
    df_but_masc=pd.read_csv('but.csv',encoding="ISO-8859-1")

    #TRAITEMENT DES DONNÉES
    df_but_masc['Année']=df_but_masc['CDM']
    df_but_fem['Année']=df_but_fem['CDM']
    df_but_masc['Année'],df_but_masc['CDM']=split_columns(df_but_masc['CDM'], df_but_masc['Année'])
    df_but_fem['Année'],df_but_fem['CDM']=split_columns(df_but_fem['CDM'], df_but_fem['Année'])

    #traduction des noms des pays
    traduction(df_CM_feminin['nom_français'])
    traduction(df_CM_masculin['nom_français'])
    traduction(df_coord['CDM']) #création d'une nouvelle colonne correspondant à la traduction d'une autre

    #on change les valeurs qui ne sont pas bien écrites
    fonction_correspondance(df_CM_masculin['nom_français'])
    fonction_correspondance(df_CM_feminin['nom_français'])
    fonction_correspondance(df_coord['CDM'])
    fonction_correspondance(df_but_masc['CDM'])
    fonction_correspondance(df_but_fem['CDM'])

    #Mettre le nom des pays au bon format
    #On merge les deux dataframes respectivement avec celle des pays
    #puis on supprimme toutes les lignes pour lesquelles nous n'avons pas de date car ce sont des lignes où les pays n'ont pas participé à la CDM
    #on supprime aussi les valeurs pour lesquelles le code alpha3 n'existe plus. généralement c'est parce que le pays n'existe plus; ex: Yougoslavie
    df_CM_masculin=pd.merge(df_CM_masculin,df_pays,on='nom_français',how='outer').dropna(subset=['Année','alpha3'])
    df_CM_feminin=pd.merge(df_CM_feminin,df_pays,on='nom_français',how='outer').dropna(subset=['Année', 'alpha3'])
    df_coord_fem=pd.merge(df_coord,df_CM_feminin,on='alpha2',how='outer').dropna(subset=['Année', 'alpha3'])
    df_coord_masc=pd.merge(df_coord,df_CM_masculin,on='alpha2',how='outer').dropna(subset=['Année', 'alpha3'])

    #suppression des duplicats et remise à niveau des index
    df_coord_fem=df_coord_fem.drop_duplicates(subset='CDM')
    df_coord_fem=df_coord_fem.reset_index(drop=True)
    df_coordfem=df_coord_fem

    df_coord_masc=df_coord_masc.drop_duplicates(subset='CDM')
    df_coord_masc=df_coord_masc.reset_index(drop=True)
    df_coordmasc=df_coord_masc

    #Modification des années du tournoi féminin (certaines n'étaient pas au bon format)
    for i in range(len(df_CM_feminin["Année"])): #on modifie le format des années qui ne sont pas écrites en entier
        if df_CM_feminin["Année"][i]<50: #si le nombre est inférieur à 50, on lui ajoute 2000
            df_CM_feminin["Année"][i]=2000+df_CM_feminin["Année"][i]
        if df_CM_feminin["Année"][i]>50 and df_CM_feminin['Année'][i]<100: #si le nombre est supérieur à 50 et inférieur à 100, on ajoute 1900
            df_CM_feminin['Année'][i]=1900+df_CM_feminin['Année'][i]
#--------------------------------------------------------------------------------------
    #Mongo

    client = pymongo.MongoClient("localhost:27017") #on créé le client
    database = client['CM'] #on crée la database CM
    collection_CMmasc = database['CM_masculin'] #création de la collection de la CM masculine
    collection_CMfem=database['CM_feminin'] #création de la collection de la CM féminine

    #on vide les collections pour éviter qu'il y ait un problème à chaque compilation du code
    collection_CMfem.drop()
    collection_CMmasc.drop()

    #insertion des dataframes dans les collections
    collection_CMmasc.insert_many(df_CM_masculin.to_dict(orient='records'))
    collection_CMfem.insert_many(df_CM_feminin.to_dict(orient='records'))

    #on créé deux listes qui stockent les codes des équipes et le nombre de fois où les pays ont été dans les 4 premiers du tournoi
    Meilleur_masc_x,Meilleur_masc_y=cursor_to_liste(collection_CMmasc.aggregate([{"$group":{"_id":"$alpha3", "nombre_dans_4_premiers_fem":{"$sum":1}}}]))
    Meilleur_fem_x,Meilleur_fem_y=cursor_to_liste(collection_CMfem.aggregate([{"$group":{"_id":"$alpha3", "nombre_dans_4_premiers_fem":{"$sum":1}}}])) 
#-----------------------------------------------------------------------------------------
    #Graphiques

    #Graphiques montrant le nombre de fois pour lesquels chaque pays a été dans les 4 premiers du classement
    graph_meilleur_fem=plt.bar(Meilleur_fem_x, Meilleur_fem_y,1.0,color='b') #CM féminin
    plt.savefig('graph1.png')#on enregistre dans le fichier graph1.png

    plt.clf()#on supprime ce qui était dans la figure pour éviter que les deux graphiques ne se superposent
    f, graph_meilleur_masc = plt.subplots(figsize=(18,5))
    graph_meilleur_masc=plt.bar(Meilleur_masc_x, Meilleur_masc_y,1.0,color='r')#CM masculin
    plt.savefig('graph2.png')#on enregistre dans le fichier graph2.png

#Création des cartes

    #carte féminine
    longitude_fem=df_coordfem['longitude'] #stockage des longitudes dans cette valeur
    latitude_fem=df_coordfem['latitude'] #stockage des latitudes dans cette valeur
    pays_fem=df_coordfem['alpha3'] #stockages des codes alpha3 dans cette valeur

    map_fem=folium.Map(location=[46.227638,2.213749], tiles='OpenStreetMap', zoom_start=2)#initialisation de la carte des pays participants(CDM fem)

    for i in range(len(df_coordfem)):#on parcourt le dataframe contenant les coordonnées des pays participants aux CDM féminines
        folium.Marker(location=[latitude_fem[i],longitude_fem[i]], popup =pays_fem[i],icon=folium.Icon(color="gray", icon='cloud'),show=True).add_to(map_fem)

    map_fem.save(outfile='map_fem.html')#enregistrement de la map

    #carte masculine
    longitude_masc=df_coordmasc['longitude'] #stockage des longitudes dans cette valeur
    latitude_masc=df_coordmasc['latitude'] #stockage des latitudes dans cette valeur
    pays_masc=df_coordmasc['alpha3'] #stockages des codes alpha3 dans cette valeur

    map_masc=folium.Map(location=[46.227638,2.213749], tiles='OpenStreetMap', zoom_start=2)#initialisation de la carte des pays participants(CDM masc)

    for i in range(len(df_coordmasc)):#on parcourt le dataframe contenant les coordonnées des pays participants aux CDM masculines
        folium.Marker(location=[latitude_masc[i],longitude_masc[i]], popup =pays_masc[i],icon=folium.Icon(color="darkred", icon='cloud'),show=True).add_to(map_masc)

    map_masc.save(outfile='map_masc.html')#enregistrement de la map

#----------------------------------------------------------------------------------------------
 
    app = dash.Dash(__name__)#création du dashboard

    #CRÉATION DES GRAPHS QUI VONT SERVIR POUR L'APPLICATION
    fig = px.bar(x=Meilleur_fem_x, y=Meilleur_fem_y,title=("Graphique barres représentant le nombre de fois où chaque équipe a été dans les 4 premiers du classement (CM_féminine)"))
    fig_masc=px.bar(x=Meilleur_masc_x, y=Meilleur_masc_y,title="Graphique barres représentant le nombre de fois où chaque équipe a été dans les 4 premiers du classement (CM_masculine)")

    app.layout = html.Div(children=[  

        html.H1(children='Dashboard sur les coupes du mondes de football (féminines et masculines)', style={'textAlign': 'center'}),#titre général du dashboard

        dcc.Tabs(style={'borderTop':'3px solid #212121', 'borderRadius':'6px', 'boxShadow':'2px 2px 30px #a4b0be'}, colors={'background':'#dfe4ea'}, id="tabs", children=[   #création des différents "onglets"

            dcc.Tab(label="Présentation", children=[   #premier onglet
                html.Div(children=[
                    html.H1(children='Présentation du projet', style={'textAlign' :'center','background-color':'#dfe4ea'}),#titre de la page
                    dcc.Textarea(
                        id='présentation',#id 
                        title='Présentation du dashboard',#titre en haut de la page
                        value='Bienvenue!\n\nNous sommes Sarah Behanzin, Amine Belgacem et Shayan Arnal.\nOn étudie ici les statistiques des différentes coupes de monde de football de 1930 à 2018.\nLes bases de données scrappées comportent des informations en plus que celles dues au scrapping, notamment avec des merges sur différentes dataframes.',
                        style={'fontFamily':'Arial','width':'100%', 'height':'1000', 'textAlign':'left', 'background-color':'#dfe4ea', 'font-size':'medium', 'font-style':'normal', 'resize':'none', 'border':'none'},
                        readOnly='readOnly',#en lecture seule
                        draggable='false',
                        rows='5'#5 lignes
                    ),

                    html.H1(children='Base de donnée importée : Liste des pays', style={'textAlign':'left'}),#première dataframe
                    dash_table.DataTable( #affichage de la base de donnée 
                        data=df_pays.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_pays.columns],
                        page_action='native',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'},
                        page_current= 0,
                        page_size= 10,
                        filter_action="native"
                    ),

                    html.H1(children='Base de donnée scrappée : Coupe du monde masculine', style={'textAlign':'left'}),#deuxième dataframe
                    dash_table.DataTable(#affichage de la base de donnée 
                        data=df_CM_masculin.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_CM_masculin.columns],
                        page_action='native',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'},
                        page_current= 0,
                        page_size= 10,
                        filter_action="native"
                    ),

                    html.H1(children='Base de donnée scrappée : Coupe du monde féminine', style={'textAlign':'left'}),#deuxième dataframe
                    dash_table.DataTable(#affichage de la base de donnée 
                        data=df_CM_feminin.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_CM_feminin.columns],
                        page_action='native',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'},
                        page_current= 0,
                        page_size= 10,
                        filter_action="native"
                    ),
                    html.H1(children='Base de donnée scrappée : Coordonnées géographiques des pays du monde', style={'textAlign':'left'}),#deuxième dataframe
                    dash_table.DataTable(#affichage de la base de donnée 
                        data=df_coord.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_coord.columns],
                        page_action='native',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'},
                        page_current= 0,
                        page_size= 10,
                        filter_action="native"
                    ),
                    html.H1(children='Base de donnée scrappée : But des 4 premiers - CDM masculine', style={'textAlign':'left'}),#deuxième dataframe
                    dash_table.DataTable(#affichage de la base de donnée 
                        data=df_but_masc.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_but_masc.columns],
                        page_action='native',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'},
                        page_current= 0,
                        page_size= 10,
                        filter_action="native"
                    ),
                    html.H1(children='Base de donnée scrappée : But des 4 premiers - CDM féminine', style={'textAlign':'left'}),#deuxième dataframe
                    dash_table.DataTable(#affichage de la base de donnée 
                        data=df_but_fem.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_but_fem.columns],
                        page_action='native',
                        fixed_rows={'headers': True},
                        style_table={'overflowY': 'auto'},
                        page_current= 0,
                        page_size= 10,
                        filter_action="native"
                    )
                ])
            ]),

            dcc.Tab(label="Analyse par les graphiques", children=[   #deuxième onglet
                html.Div(children=[
                    html.H1(children='Différents graphiques', style={'textAlign' :'center', 'background-color':'#dfe4ea'}),#titre de la page
                        dcc.Textarea(
                        id='histo',
                        title='Graphiques',
                        value='Voici les graphiques barres représentant le nombre de fois où chaque pays a été dans les 4 premiers du classement.\nSi vous voulez voir à quels pays les codes correspondent, vous pouvez les rechercher dans la  première base de données présente dans le précédent onglet ',
                        style={'fontFamily':'Arial','width':'100%', 'height':'1000', 'textAlign':'left', 'background-color':'#dfe4ea', 'font-size':'medium', 'font-style':'normal', 'resize':'none','border':'none'},
                        readOnly='readOnly',
                        draggable='false',
                        rows='2'
                    ),
                        dcc.Graph(#affichage du quatrième graph
                            id='graph1',
                            figure=fig,
                            style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px'}
                        ),
                         dcc.Graph(#affichage du quatrième graph
                            id='graph2',
                            figure=fig_masc,
                            style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px'}
                        ),
                        dcc.Graph(
                            figure={
                                'data': [
                                    {'x': Meilleur_fem_x, 'y': Meilleur_fem_y, 'type': 'bar', 'name': 'CM_Femme'},
                                    {'x': Meilleur_masc_x, 'y': Meilleur_masc_y, 'type': 'bar', 'name': u'CM_Homme'},
                                ],
                                'layout': {
                                    'title': 'Comparaison des des pays arrivés dans les 4 premiers pour la Coupe du Monde Féminine et Masculine'
                                }
                            }
                        )
                ]),
            ]),

            dcc.Tab(label="Cartes des pays participants", children=[   #quatrième onglet

                html.Div(children=[
                    html.H1(children='Cartes', style={'textAlign' :'center', 'background-color':'#dfe4ea'}),#titre de la page
                    html.H1(children='Cartes des pays ayant particpé aux coupes du mondes féminines', style={'textAlign':'left'}),#titre de la première carte
                      html.Iframe(#affichage de la première map
                        id='map1',
                        srcDoc=open('map_fem.html','r').read(),
                        width='60%',
                        height='600',
                        style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px', 'margin':'25'}
                    ),
                    html.H1(children='Cartes des pays ayant particpé aux coupes du mondes masculines', style={'textAlign':'left'}),#titre de la deuxième carte
                    html.Iframe(#affichage de la première map
                        id='map2',
                        srcDoc=open('map_masc.html','r').read(),
                        width='60%',
                        height='600',
                        style={'boxShadow':'2px 2px 30px #a4b0be', 'borderRadius':'10px', 'margin':'25'}
                    )
                ])
            ])    
        ])
    ])

    app.run_server(debug=True)

    return None


if __name__ == '__main__':
    main()