import requests
from bs4 import BeautifulSoup

with open('urls.txt','r') as file:
    # with open('pays.csv','w') as outf:
    #     outf.write('Rang , equipe\n')
        for row in file: #pour chaque lien du fichier 
            url = row.strip() #je passe le lien en url et j'enleve le retour à la ligne avec la fonction strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                rank =  soup.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
                name = soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3')
                print(rank.text+' '+':'+' '+name.text)
                # outf.write(rank.text+' '+':'+' '+name.text+'\n')