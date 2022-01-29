
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
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    df_coord=pd.read_csv('coord.csv')
    df_but_fem=pd.read_csv('but_f.csv')
    df_but_masc=pd.read_csv('but.csv')

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
    df_coord_fem=pd.merge(df_coord,df_CM_masculin,on='alpha2',how='outer').dropna(subset=['Année', 'alpha3'])

  

    #Modification des années du tournoi féminin (certaines n'étaient pas au bon format)
    for i in range(len(df_CM_feminin["Année"])): #on modifie le format des années qui ne sont pas écrites en entier
        if df_CM_feminin["Année"][i]<50: #si le nombre est inférieur à 50, on lui ajoute 2000
            df_CM_feminin["Année"][i]=2000+df_CM_feminin["Année"][i]
        if df_CM_feminin["Année"][i]>50 and df_CM_feminin['Année'][i]<100: #si le nombre est supérieur à 50 et inférieur à 100, on ajoute 1900
            df_CM_feminin['Année'][i]=1900+df_CM_feminin['Année'][i]

    #Mongo
    
    client = pymongo.MongoClient("localhost:27017") #on créé le client
    database = client['CM'] #on crée la database CM
    collection_CMmasc = database['CM_masculin'] #création de la collection de la CM masculine
    collection_CMfem=database['CM_feminin'] #création de la collection de la CM féminine
    collection_but_masc=database['But_masculin']#création de la collection But masculin
    collection_but_fem=database['But_feminin']#création de la collection But féminin
    

    #on vide les collections pour éviter qu'il y ait un problème à chaque compilation du code
    collection_CMfem.drop()
    collection_CMmasc.drop()
    collection_but_masc.drop()

    #insertion des dataframes dans les collections
    collection_CMmasc.insert_many(df_CM_masculin.to_dict(orient='records'))
    collection_CMfem.insert_many(df_CM_feminin.to_dict(orient='records'))
    collection_but_masc.insert_many(df_but_masc.to_dict(orient='records'))
    collection_but_fem.insert_many(df_but_fem.to_dict(orient='records'))

    #on créé deux listes qui stockent les codes des équipes et le nombre de fois où les pays ont été dans les 4 premiers du tournoi
    Meilleur_masc_x,Meilleur_masc_y=cursor_to_liste(collection_CMmasc.aggregate([{"$group":{"_id":"$alpha3", "nombre_dans_4_premiers_fem":{"$sum":1}}}]))
    Meilleur_fem_x,Meilleur_fem_y=cursor_to_liste(collection_CMfem.aggregate([{"$group":{"_id":"$alpha3", "nombre_dans_4_premiers_fem":{"$sum":1}}}])) 
    But_masc_x,But_masc_y=cursor_to_liste(collection_but_masc.aggregate([{"$group":{"_id":"$equipe", "moyene_buts":{"$avg":"$Goals"}}}]))
    But_fem_x,But_fem_y=cursor_to_liste(collection_but_fem.aggregate([{"$group":{"_id":"$equipe", "moyene_buts":{"$avg":"$Goals"}}}]))
    
    #graph pie

    graph_pie=make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    graph_pie.add_trace(go.Pie(labels=But_masc_x, values=But_masc_y, name="CDM masculin"),1, 1)
    graph_pie.add_trace(go.Pie(labels=But_fem_x, values=But_fem_y, name="CDM féminin"),1, 2)

    graph_pie.update_layout(
    title_text="Moyenne de buts faits par les pays arrivés dans les 4 premiers de 1930 à 2018",
    annotations=[dict(text='CDM_masc', x=0.18, y=0.5, font_size=20, showarrow=False), dict(text='CDM_fem', x=0.82, y=0.5, font_size=20, showarrow=False)])

    graph_pie.show()
    # graph_pie_masc=px.pie(values=But_masc_y,names=But_masc_x,color_discrete_sequence=px.colors.sequential.RdBu, title='Pourcentage des pays ayant été dans les 4 premiers de 1930 à 2018')
    # graph_pie_masc.show()
   
    #Création des cartes

    df_coord_fem=df_coord_fem.drop_duplicates(subset='CDM')
    df_coord_fem=df_coord_fem.reset_index(drop=True)
    df_coordfem=df_coord_fem

    longitude_fem=df_coordfem['longitude']
    latitude_fem=df_coordfem['latitude']
    pays_fem=df_coordfem['alpha3']

    map_fem=folium.Map(location=[46.227638,2.213749], tiles='OpenStreetMap', zoom_start=2.5)

    for i in range(len(df_coordfem)):
        folium.Marker(location=[latitude_fem[i],longitude_fem[i]], popup =pays_fem[i],icon=folium.Icon(color="gray", icon='cloud'),show=True).add_to(map_fem)

    map_fem.save(outfile='map_fem.html')

    return None

if __name__ == '__main__':
    main()