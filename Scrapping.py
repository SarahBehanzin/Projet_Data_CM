'''
authors:
    sarah.behanzin@edu.esiee.fr
    mohammad-amine.belgacem@edu.esiee.fr
    shayan.arnal@edu.esiee.fr
'''

from cgi import test
from cgitb import text
from cmath import nan
from os import name
import string
from numpy import NaN
import requests
import string
from bs4 import BeautifulSoup

def main():

     #SCRAPPING DES DONNÉES CDM MASCULIN
    main_url = "https://www.fifa.com/fr/tournaments/mens/worldcup"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    all_href = [elt['href'] for elt in soup.findAll('a') if elt.get('href')  ]#On recupere tous les liens de la page 
    #On recupere ensuite les liens de toutes les cdm
    all_tournaments = ['https://www.fifa.com'+elt for elt in all_href if '/fr/tournaments/mens/worldcup/canadamexicousa2026'!= elt and '/fr/tournaments/mens/worldcup/qatar2022'!=elt if '/fr/tournaments/mens/worldcup/' in elt]

    with open('pays.csv','w') as outf:   #pour pouvoir stocker les données des pays que l'on va scapper
        outf.write('Année,Dates de début,Dates de fin,Rang,nom_français\n') #permet de renseigner la premiere ligne de notre csv qui corresponds au nom des colonnes
        with open('but.csv','w') as sortie:  #pour pouvoir stocker les données des buts des pays que l'on va scapper
            sortie.write('CDM,equipe,Goals\n') #permet de renseigner la premiere ligne de notre csv qui corresponds au nom des colonnes 
            for row in all_tournaments: #pour chaque lien de cdm de la liste  
                url = row
                response2 = requests.get(url, headers=headers)
                soup_tournoi = BeautifulSoup(response2.text, 'html.parser')
                phrase = soup_tournoi.find('div',{'class':'col'}).find('h1').text #correspond à la phrase contenant la date du tournoi
                annee=[]
                for i in range(len(phrase)):
                    if phrase[i] in string.digits:
                        annee.append(phrase[i])

                #---------------
                #le site est fait de la maniere suivante :
                # - il y a une div qui contient les 4 finalistes et leur classement dans des div différentes.
                # On crée une boucle qui va parcourir cette div principale et recupérer le classement et le nom de l'equipe pour chaque coupe du monde présent dans la liste 

                div_rank =  soup_tournoi.find_all('a',{'class':'fp-tournament-standing_standingRow__mPKma'})
                for i in div_rank :
                    rank = i.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
                    name_2 = i.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text

                #---------------

                        #l'année est composée des différents chiffres de la liste "annee" qui a été conçue au dessus
                    year=''
                    for i in range(len(annee)):
                        year+=annee[i]


                    #pour les dates, on split les dates de début et de fin grâce au "-" et on affecte les deux valeurs dans les bonnes colonnes
                    dates = soup_tournoi.find('div',{'class':'col'}).find('h6').text
                    dates_liste=dates.split("-")
                    date_debut=dates_liste[0]
                    date_fin=dates_liste[1]
                    #-------------------

                    #cette ligne de code permets de stocker les données dans le fichier pays 
                    outf.write(year+','+date_debut+','+date_fin+','+rank.text+','+name_2+'\n')

                #---------------
                #On va maintenant récuperer les différentes coupe du monde renseignant le nombre de but des équipes placées sur le podium.
                
                cdm = soup_tournoi.find('div',{'class':'fp-tournament-standing_hero__text__2G3_Z'}).find('h6') #on récupere la coupe du monde en question

                #---------------
                #On decide maintenant de vouloir récupérer le nombre de buts des 4 finalistes de chaque coupe du monde 
                
                for j in soup_tournoi.find_all('a',{'class':'fp-tournament-standing_standingRow__mPKma'}) : # - on commence par parcourir la div principale où est stocker les informations des 4 finalistes.
                    if j.get('href'):
                        x = 'https://www.fifa.com'+j['href'] # - ensuite, on recupere le lien qui mène à la page où est stocker l'information sur les buts
                        response3 = requests.get(x, headers=headers) # - ce lien va devenir notre base pour scrapper et nous créeons un beautiful soup en fonction de celui-ci
                        soup_equipe = BeautifulSoup(response3.text, 'html.parser') #  pour nous permettre de recuperer les données de la page  

                        # - Aprés analyse du site on remarque que nous devons faire quelques exceptions : 
                        # - pour la cdm 2018, dans le lien où sont stockées les informations de l'équipe, 
                        # le nombre de buts corresponds à la deuxième div alors que pour toutes les autres, c'est la 1ère.
                        # comme toutes les divs sont faites en fonction de la meme classe, on commence par toutes les parcourir.
                        
                        if '2018russia' in x:
                            for i in soup_equipe.find_all('div',{'class':'fp-stat-card-vertical_card__krJHI undefined'}): 
                                y = i.find('h6').text
                                if y == 'Goals': #lorsque dans la div, le titre sous h6 est égale à Goals
                                    goal = i.find('h2') # on recupere ce qui est compris dans h2, c'est à dire le nombre de but 
                                    nom_equipe = soup_equipe.find('div',{'class':'fp-team-banner_Team__3SPEH'}).find('h1') # on recupere le nom de l'equipe 
                                    sortie.write(cdm.text[27:-1]+","+ nom_equipe.text + "," + goal.text+'\n')
                                # cette ligne permets de renseigner dans le fichier but.csv :
                                # - en premier : la cdm et avec le [27:-1] cela permets de selectionner la zone de texte à prendre et 
                                # de juste récuperer les nom du pays organisateur et l'année 
                                # - le nom de l'equipe
                                # - le nombre de buts  

                        # la deuxième exception a faire concerne la cdm de 1982
                        # pour l'affichage dans le fichier but.csv, comme il n'y a pas de logo TM, 
                        # on est pas obliger de rensigner le -1 dans les crochets.

                        
                        elif '1982spain' in x :
                            goal = soup_equipe.find('div',{'class':'fp-stat-card-vertical_card__krJHI undefined'}).find('h2')
                            nom_equipe = soup_equipe.find('div',{'class':'fp-team-banner_Team__3SPEH'}).find('h1')
                            sortie.write(cdm.text[27:]+","+ nom_equipe.text + "," + goal.text+'\n') 
                        
                        #Sinon on recupere pour toutes les autres cdm, la cdm correspondant accompagné du nom de l'equipe et de son nombre de buts marqués.
                        else:
                            goal = soup_equipe.find('div',{'class':'fp-stat-card-vertical_card__krJHI undefined'}).find('h2')
                            nom_equipe = soup_equipe.find('div',{'class':'fp-team-banner_Team__3SPEH'}).find('h1')
                            sortie.write(cdm.text[27:-1]+","+ nom_equipe.text + "," + goal.text+'\n')


                



    #SCRAPPING DES DONNÉES CDM FEMININ
    main_url_f = "https://www.fifa.com/fr/tournaments/womens/womensworldcup"
    headers_f = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response_f = requests.get(main_url_f, headers=headers_f)
    soup_f = BeautifulSoup(response_f.text, 'html.parser')

    all_href_f = [elt['href'] for elt in soup_f.findAll('a') if elt.get('href')  ] #On recupere tous les liens de la page 
    #On recupere ensuite les liens de toutes les cdm   
    all_tournaments_f = ['https://www.fifa.com'+elt for elt in all_href_f if '/fr/tournaments/womens/womensworldcup/australia-new-zealand2023'!= elt if '/fr/tournaments/womens/womensworldcup/' in elt]
    

    #On scrapp les données de la page de la même manière vu que les deux liens sont codés de manière identique.
    #On a juste quelque exception à faire qui change.

    with open('pays_f.csv','w') as outf:
        outf.write('Année,Dates de début,Dates de fin,Rang,nom_français\n')
        with open('but_f.csv','w') as sortie:
            sortie.write('CDM,equipe,Goals\n')
            for row in all_tournaments_f: #pour chaque lien de la liste  
                url = row
                response2 = requests.get(url, headers=headers)
                soup_tournoi = BeautifulSoup(response2.text, 'html.parser')
                phrase = soup_tournoi.find('div',{'class':'col'}).find('h1').text #correspond à la phrase contenant la date du tournoi
                annee=[]
                for i in range(len(phrase)):
                    if phrase[i] in string.digits:
                        annee.append(phrase[i])

            

                div_rank =  soup_tournoi.find_all('a',{'class':'fp-tournament-standing_standingRow__mPKma'})
                for i in div_rank :
                    rank = i.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
                    name_2 = i.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3').text

                    #---------------

                        #l'année est composée des différents chiffres de la liste "annee" qui a été conçue au dessus
                    year=''
                    for i in range(len(annee)):
                        year+=annee[i]


                    #pour les dates, on split les dates de début et de fin grâce au "-" et on affecte les deux valeurs dans les bonnes colonnes
                    dates = soup_tournoi.find('div',{'class':'col'}).find('h6').text
                    dates_liste=dates.split("-")
                    date_debut=dates_liste[0]
                    date_fin=dates_liste[1]
                    #-------------------

                    outf.write(year+','+date_debut+','+date_fin+','+rank.text+','+name_2+'\n')

                #---------------
                #On va maintenant récuperer les différentes coupe du monde renseignant le nombre de but des équipes placées sur le podium.


                cdm = soup_tournoi.find('div',{'class':'fp-tournament-standing_hero__text__2G3_Z'}).find('h6') #on récupere la coupe du monde en question

                for j in soup_tournoi.find_all('a',{'class':'fp-tournament-standing_standingRow__mPKma'}) :
                    if j.get('href'):
                        x = 'https://www.fifa.com'+j['href']
                        response3 = requests.get(x, headers=headers)
                        soup_equipe = BeautifulSoup(response3.text, 'html.parser')
                        
                        #Ici on réalise la même exception que faite pour la cdm masculain de russia2018 
                        
                        if 'france2019' in x:
                            for i in soup_equipe.find_all('div',{'class':'fp-stat-card-vertical_card__krJHI undefined'}):
                                y = i.find('h6').text
                                if y == 'Goals':
                                    goal = i.find('h2')
                                    nom_equipe = soup_equipe.find('div',{'class':'fp-team-banner_Team__3SPEH'}).find('h1')
                                    sortie.write(cdm.text[36:-1]+","+ nom_equipe.text + "," + goal.text+'\n')
                       
                        #ici, on realise une exception dans l'affichage de la cdm dans le fichier csv pour 4 cdm précise.
                        # le texte où est renseigné le nom de la cdm est plus long que les autres, donc pour pouvoir récuprer juste le 
                        # nom du pays organisateur et l'année, on decale encorer la zone de texte à prendre.

                        elif 'chinapr1991' in x or 'sweden1995' in x or 'usa1999' in x  or 'usa2003' in x :
                            goal = soup_equipe.find('div',{'class':'fp-stat-card-vertical_card__krJHI undefined'}).find('h2')
                            nom_equipe = soup_equipe.find('div',{'class':'fp-team-banner_Team__3SPEH'}).find('h1')
                            sortie.write(cdm.text[47:-1]+","+ nom_equipe.text + "," + goal.text+'\n')
                        else:
                            goal = soup_equipe.find('div',{'class':'fp-stat-card-vertical_card__krJHI undefined'}).find('h2')
                            nom_equipe = soup_equipe.find('div',{'class':'fp-team-banner_Team__3SPEH'}).find('h1')
                            sortie.write(cdm.text[36:-1]+","+ nom_equipe.text + "," + goal.text+'\n')

    #SCRAPPING DES DONNÉES GÉOGRAPHIQUES

        #SCRAPPING DES NOMS DES STADES DES FINALES

    main_url_liste = "https://www.maxifoot.fr/palmares-coupe-du-monde.htm"
    headers_liste = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response_liste = requests.get(main_url_liste, headers=headers_liste)
    soup_liste = BeautifulSoup(response_liste.text, 'html.parser')
    all_liste=soup_liste.find_all(class_='l1')
    liste_stades=[]

    for i in range(len(all_liste)):
        liste_stades.append(all_liste[i].text.split(',')[1])
        for j in range(len(liste_stades)):
            if liste_stades[j]=='':
                del liste_stades[j]

        #SCRAPPING DES COORDONNEES GEOGRAPHIQUE DES PAYS DU MONDE
    main_url = "https://developers.google.com/public-data/docs/canonical/countries_csv"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response_coord = requests.get(main_url, headers=headers)
    soup_coord = BeautifulSoup(response_coord.text, 'html.parser')
    compteur = 0

    #comme le site est codé de manière trés simple avec aucune différence entre les différents td.
    #Aprés analyse du site, on voit que tous les infos sont par blocs de 4 lignes.
    #on crée une variable compteur qui s'increment lors du parcours de tous les td et qui va nous servir de selecteur de l'information.
    #En fonction du reste de la division entre le compteur et 4, cela nous permettre d'identifier la donnée scrappée.
    with open('coord.csv','w') as outf:
        outf.write('alpha2,latitude,longitude,CDM\n')
        for i in soup_coord.find_all('td'):
            compteur = compteur +1
            if compteur%4==1: # on recupere la donnée du code du Pays 
                outf.write(i.text+',')
                #print(i.text)
            if compteur%4==2: # on recupere la donnée de latitude
                outf.write(i.text+',')
                #print(i.text)
            if compteur%4==3: # on recupere la donnée de longitude 
                outf.write(i.text+',')
                #print(i.text)
            if compteur%4==0: # on recupere la donnée du nom du pays
                outf.write(i.text+'\n')
                #print(i.text+'\n')

    return None

if __name__ == '__main__':
    main()
