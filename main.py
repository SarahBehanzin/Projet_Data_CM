from cgitb import text
from os import name
import string
import pandas as pd
import requests
import string
from googletrans import Translator
from bs4 import BeautifulSoup


translator=Translator()

#FONCTIONS

# def fonction_correspondance(mot_entre):
#     mot_entre=mot_entre.lower()
#     if mot_entre=="match pour la troisième place" or  mot_entre=="play-off for third place" or  mot_entre=="match for 3rd place" or mot_entre=="MATCH FOR 3RD PLACE":
#         mot="MATCH FOR 3RD PLACE"
#     if mot_entre=="demi-finales" or mot_entre== "semi-final" or mot_entre=="SEMIFINALS":
#         mot="SEMIFINALS"
#     if mot_entre=="quarts de finale" or mot_entre== "quarter-final" or mot_entre=="quarterfinals" or mot_entre=="quarter Finals" or mot_entre=="QUARTER FINAL":
#         mot="QUARTER FINAL"
#     if mot_entre=="huitièmes de finale" or mot_entre=="round of 16" or mot_entre=="round of sixteen":
#         mot="round of sixteen"
#     if mot_entre=="République Fédérale d'Allemagne":
#         mot="allemagne"
#     if mot_entre=="russie" or mot_entre=="urs":
#         mot="russia"
#     else:
#         mot=mot_entre
#     return mot

def fonction_pays(nom_pays):
    nom_pays=nom_pays.lower()
    nom_final=nom_pays[0:3]
    return nom_final

def traduction(nom):
#    nom.lower()
    nom_final=translator.translate(nom, dest='en').text
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
        outf.write('Année,Dates de début,Dates de fin,Rang,Equipe\n')
        for row in all_tournaments: #pour chaque lien de la liste  
            url = row
            response = requests.get(url, headers=headers)
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

                 #on s'assure que les noms des pays soient les bons et dans la bonne langue
                if name_2=="République Fédérale d'Allemagne":
                    name_2="Allemagne"
                #name=fonction_correspondance(name)
                name_2=traduction(name_2)

                #-------------------

                outf.write(year+','+date_debut+','+date_fin+','+rank.text+','+name_2+'\n')
            # outf.write(year+','+date_debut+','+date_fin+','+name+'\n')


    #SCRAPPING DES DONNÉES CDM FEMININ
    main_url_f = "https://www.fifa.com/fr/tournaments/womens/womensworldcup"
    headers_f = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response_f = requests.get(main_url_f, headers=headers_f)
    soup_f = BeautifulSoup(response_f.text, 'html.parser')
    all_href_f = [elt['href'] for elt in soup_f.findAll('a') if elt.get('href')  ]
    all_tournaments_f = ['https://www.fifa.com'+elt for elt in all_href_f if '/fr/tournaments/womens/womensworldcup/australia-new-zealand2023'!= elt if '/fr/tournaments/womens/womensworldcup/' in elt]

    with open('pays_f.csv','w') as outf:
        outf.write('Année,Dates de début,Dates de fin,Vainqueur\n')
        for row in all_tournaments_f: #pour chaque lien de la liste  
            url = row
            response = requests.get(url, headers=headers_f)
            soup = BeautifulSoup(response.text, 'html.parser')
            phrase = soup.find('div',{'class':'col'}).find('h1').text
            annee=[]
            for i in range(len(phrase)):
                if phrase[i] in string.digits:
                    annee.append(phrase[i])

            #l'année est composée des différents chiffres de la liste "annee" qui a été conçue au dessus
            year=''
            for i in range(len(annee)):
                year+=annee[i]

            #pour les dates, on split les dates de début et de fin grâce au "-" et on affecte les deux valeurs dans les bonnes colonnes
            dates = soup.find('div',{'class':'col'}).find('h6').text
            dates_liste=dates.split("-")
            date_debut=dates_liste[0]
            date_fin=dates_liste[1]

            name = soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text#nom du vainqueur

            #on s'assure que les noms des pays soient les bons et dans la bonne langue
            # if name=="République Fédérale d'Allemagne":
            #     name="Allemagne"
            name=traduction(name)

            outf.write(year+','+date_debut+','+date_fin+','+name+'\n')


#------------------------------------------------------------------------------------------------------------------------------------------------#

            
    #METTRE LES DONNÉES SOUS FORME DE DATAFRAME
    df_CM_masculin=pd.read_csv('pays.csv')#on lit les données stockées dans le bon fichier csv
    df_CM_feminin=pd.read_csv('pays_f.csv')#on lit les données stockées dans le bon fichier csv

    #TRAITEMENT DES DONNÉES
    #CM mascumlin
    df_CM_masculin["Code_pays"]=df_CM_masculin["Equipe"]
    for i in range(len(df_CM_masculin)):
        df_CM_masculin["Code_pays"][i]=fonction_pays(df_CM_masculin["Code_pays"][i])

    # #CM feminin
    # df_CM_feminin["Code_pays"]=df_CM_feminin["Equipe"]
    # for i in range(len(df_CM_feminin)):
    #     df_CM_feminin["Code_pays"][i]=fonction_pays(df_CM_feminin["Code_pays"][i])

    for i in range(len(df_CM_feminin["Année"])): #on modifie le format des années qui ne sont pas écrites en entier
        if df_CM_feminin["Année"][i]<50: #si le nombre est inférieur à 50, on lui ajoute 2000
            df_CM_feminin["Année"][i]=2000+df_CM_feminin["Année"][i]
        if df_CM_feminin["Année"][i]>50 and df_CM_feminin['Année'][i]<100: #si le nombre est supérieur à 50 et inférieur à 100, on ajoute 1900
            df_CM_feminin['Année'][i]=1900+df_CM_feminin['Année'][i]

    print(df_CM_masculin)
    return None


if __name__ == '__main__':
    main()