import requests
from bs4 import BeautifulSoup

main_url = "https://www.fifa.com/fr/tournaments/mens/worldcup"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
response = requests.get(main_url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
all_href = [elt['href'] for elt in soup.findAll('a') if elt.get('href')  ]
all_tournaments = ['https://www.fifa.com'+elt for elt in all_href if '/fr/tournaments/mens/worldcup/canadamexicousa2026'!= elt and '/fr/tournaments/mens/worldcup/qatar2022'!=elt if '/fr/tournaments/mens/worldcup/' in elt]

for row in all_tournaments: #pour chaque lien de la liste  
    print(row)
    url = row
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank =  soup.find('div',{'class':'fp-tournament-standing_rankDescription__1sEZl'}).find('h6')
    name = soup.find('div',{'class':'fp-tournament-standing_teamName__eYSTw'}).find('h3')
    print(rank.text+' '+':'+' '+name.text)
        # outf.write(rank.text+' '+':'+' '+name.text+'\n')