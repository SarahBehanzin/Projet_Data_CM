from cgitb import text
import string
import pandas as pd
import requests
import string
from googletrans import Translator
from bs4 import BeautifulSoup
translator=Translator()
# main_url = "https://www.fifa.com/fr/tournaments/mens/worldcup"
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
# response = requests.get(main_url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
# all_href = [elt['href'] for elt in soup.findAll('a') if elt.get('href')  ]
# all_tournaments = ['https://www.fifa.com'+elt for elt in all_href if '/fr/tournaments/mens/worldcup/canadamexicousa2026'!= elt and '/fr/tournaments/mens/worldcup/qatar2022'!=elt if '/fr/tournaments/mens/worldcup/' in elt]

# with open('pays.csv','w') as outf:
#     outf.write('Vainqueur , equipe\n')
#     for row in all_tournaments: #pour chaque lien de la liste  
#         url = row
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         rank =  soup.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
#         name = soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3')
#         print(rank.text+' '+':'+' '+name.text)
#         outf.write(rank.text+' '+':'+' '+name.text+'\n')


def traduction(nom):
#    nom.lower()
    nom_final=translator.translate(nom, dest='en').text
    return nom_final

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
