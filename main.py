from cgitb import text
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
    nom_final=translator.translate(nom, dest='en').text
    nom_final=nom_final.lower()
    return nom_final



def main():
    #SCRAPPING DES DONNÉES
    main_url = "https://www.fifa.com/fr/tournaments/mens/worldcup"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_href = [elt['href'] for elt in soup.findAll('a') if elt.get('href')  ]
    all_tournaments = ['https://www.fifa.com'+elt for elt in all_href if '/fr/tournaments/mens/worldcup/canadamexicousa2026'!= elt and '/fr/tournaments/mens/worldcup/qatar2022'!=elt if '/fr/tournaments/mens/worldcup/' in elt]

    with open('pays.csv','w') as outf:
        outf.write('Année,Dates de début,Dates de fin,Vainqueur\n')
        for row in all_tournaments: #pour chaque lien de la liste  
            url = row
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            phrase = soup.find('div',{'class':'col'}).find('h1').text
            annee=[]
            for i in range(len(phrase)):
                if phrase[i] in string.digits:
                    annee.append(phrase[i])

            #l'année est composée des différents chiffres de la liste "annee" qui a été conçue au dessus
            year=''+annee[0]+annee[1]+annee[2]+annee[3]

            #pour les dates, on split les dates de début et de fin grâce au "-" et on affecte les deux valeurs dans les bonnes colonnes
            dates = soup.find('div',{'class':'col'}).find('h6').text
            dates_liste=dates.split("-")
            date_debut=dates_liste[0]
            date_fin=dates_liste[1]

            #gagnant
            #rank_win =  soup.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')

            name = soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text #nom du vainqueur
            # deux=soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text #nom du deuxième
            # trois=soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text #nom du troisième
            # quatre=soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text #nom du quatrième

            #on s'assure que les noms des pays soient les bons et dans la bonne langue
            if name=="République Fédérale d'Allemagne":
                name="Allemagne"
            #name=fonction_correspondance(name)
            name=traduction(name)

            outf.write(year+','+date_debut+','+date_fin+','+name+'\n')
            
    #METTRE LES DONNÉES SOUS FORME DE DATAFRAME
    df_CM=pd.read_csv('pays.csv')#on lit les données stockées dans le fichier csv


    #TRAITEMENT DES DONNÉES
    df_CM["Code_vainqueur"]=df_CM["Vainqueur"]
    for i in range(len(df_CM)):
        df_CM["Code_vainqueur"][i]=fonction_pays(df_CM["Vainqueur"][i])
    print(df_CM)
    return None


if __name__ == '__main__':
    main()