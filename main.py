from cgitb import text
from os import name
import string
import pandas as pd
import requests
import string
import pymongo
from googletrans import Translator
from bs4 import BeautifulSoup

translator=Translator() #fonction transmlator

#Base de données contenant la liste des pays conforme à la norme ISO 3166-1

df_pays=pd.read_csv("sql-pays.csv", names=["id ", "alpha2", "alpha3", "nom_français", "nom_anglais"]) #on lit les données et on rajoute le header car il n'était pas dans le fichier

#FONCTIONS

def fonction_correspondance(mot_entre):
    mot=[]
    for i in range(1,len(df_pays['nom_français'])):
        if (df_pays["nom_français"][i] in mot_entre) or (df_pays['nom_anglais'][i] in mot_entre):
            mot=df_pays['nom_français'][i]
    return mot

def fonction_pays(nom_pays):
    nom_final=[]
    for i in range(1,len(df_pays)):
        if df_pays['nom_français'][i]==nom_pays:
            nom_final=df_pays['alpha3'][i]
    return nom_final

def traduction(nom):
    nom_final=[]
    for i in range(1,len(df_pays)):
        if df_pays['nom_français'][i]==nom:
            nom_final=str(df_pays['nom_anglais'][i])
    return nom_final

def main():

    #SCRAPPING DES DONNÉES CDM MASCULIN
    main_url = "https://www.fifa.com/fr/tournaments/mens/worldcup"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_href = [elt['href'] for elt in soup.findAll('a') if elt.get('href')  ]
    all_tournaments = ['https://www.fifa.com'+elt for elt in all_href if '/fr/tournaments/mens/worldcup/canadamexicousa2026'!= elt and '/fr/tournaments/mens/worldcup/qatar2022'!=elt if '/fr/tournaments/mens/worldcup/' in elt]

    with open('pays.csv','w') as outf:
        outf.write('Année,Dates de début,Dates de fin,Rang,nom_français\n')
        for row in all_tournaments: #pour chaque lien de la liste  
            url = row
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            phrase = soup.find('div',{'class':'col'}).find('h1').text #correspond à la phrase contenant la date du tournoi
            annee=[]
            for i in range(len(phrase)):
                if phrase[i] in string.digits:
                    annee.append(phrase[i])

           

            div_rank =  soup.find_all('a',{'class':'fp-tournament-standing_standingRow__mPKma'})
            for i in div_rank :
                rank = i.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
                name_2 = i.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text

                #---------------

                    #l'année est composée des différents chiffres de la liste "annee" qui a été conçue au dessus
                year=''
                for i in range(len(annee)):
                    year+=annee[i]


                #pour les dates, on split les dates de début et de fin grâce au "-" et on affecte les deux valeurs dans les bonnes colonnes
                dates = soup.find('div',{'class':'col'}).find('h6').text
                dates_liste=dates.split("-")
                date_debut=dates_liste[0]
                date_fin=dates_liste[1]
                #-------------------

                outf.write(year+','+date_debut+','+date_fin+','+rank.text+','+name_2+'\n')


    #SCRAPPING DES DONNÉES CDM FEMININ
    main_url_f = "https://www.fifa.com/fr/tournaments/womens/womensworldcup"
    headers_f = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response_f = requests.get(main_url_f, headers=headers_f)
    soup_f = BeautifulSoup(response_f.text, 'html.parser')
    all_href_f = [elt['href'] for elt in soup_f.findAll('a') if elt.get('href')  ]
    all_tournaments_f = ['https://www.fifa.com'+elt for elt in all_href_f if '/fr/tournaments/womens/womensworldcup/australia-new-zealand2023'!= elt if '/fr/tournaments/womens/womensworldcup/' in elt]

    with open('pays_f.csv','w') as outf:
        outf.write('Année,Dates de début,Dates de fin,Rang,nom_français\n')
        for row in all_tournaments_f: #pour chaque lien de la liste  
            url = row
            response = requests.get(url, headers=headers_f)
            soup = BeautifulSoup(response.text, 'html.parser')
            phrase = soup.find('div',{'class':'col'}).find('h1').text
            annee=[]
            for i in range(len(phrase)):
                if phrase[i] in string.digits:
                    annee.append(phrase[i])

            div_rank =  soup.find_all('a',{'class':'fp-tournament-standing_standingRow__mPKma'})
            for i in div_rank :
                rank = i.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
                name_2 = i.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text

                #---------------

                    #l'année est composée des différents chiffres de la liste "annee" qui a été conçue au dessus
                year=''
                for i in range(len(annee)):
                    year+=annee[i]


                #pour les dates, on split les dates de début et de fin grâce au "-" et on affecte les deux valeurs dans les bonnes colonnes
                dates = soup.find('div',{'class':'col'}).find('h6').text
                dates_liste=dates.split("-")
                date_debut=dates_liste[0]
                date_fin=dates_liste[1]
                #-------------------

                outf.write(year+','+date_debut+','+date_fin+','+rank.text+','+name_2+'\n')


#------------------------------------------------------------------------------------------------------------------------------------------------#

    #METTRE LES DONNÉES SOUS FORME DE DATAFRAME
    df_CM_masculin=pd.read_csv('pays.csv')#on lit les données stockées dans le bon fichier csv
    df_CM_feminin=pd.read_csv('pays_f.csv')#on lit les données stockées dans le bon fichier csv

    #TRAITEMENT DES DONNÉES

    #Mettre le nom des pays au bon format
    #On merge les deux dataframes respectivement avec celle des pays, puis on supprimme toutes les lignes pour lesquelles nous n'avons pas de date

    df_CM_masculin=pd.merge(df_CM_masculin,df_pays,on='nom_français',how='outer').dropna(subset=['Année'])

    df_CM_feminin=pd.merge(df_CM_feminin,df_pays,on='nom_français',how='outer').dropna(subset=['Année'])

    for i in range(len(df_CM_feminin["Année"])): #on modifie le format des années qui ne sont pas écrites en entier
        if df_CM_feminin["Année"][i]<50: #si le nombre est inférieur à 50, on lui ajoute 2000
            df_CM_feminin["Année"][i]=2000+df_CM_feminin["Année"][i]
        if df_CM_feminin["Année"][i]>50 and df_CM_feminin['Année'][i]<100: #si le nombre est supérieur à 50 et inférieur à 100, on ajoute 1900
            df_CM_feminin['Année'][i]=1900+df_CM_feminin['Année'][i]

#--------------------------------------------------------------------------------------
    #Mongo
    client = pymongo.MongoClient("localhost:27017")
    database = client['CM']
    collection_CMmasc = database['CM_masculin']
    collection_CMfem=database['CM_feminin']

    collection_CMmasc.insert_many(df_CM_masculin.to_dict(orient='records'))
    collection_CMfem.insert_many(df_CM_feminin.to_dict(orient='records'))
    return None


if __name__ == '__main__':
    main()