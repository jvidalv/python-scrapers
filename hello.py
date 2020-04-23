from pprint import pprint
from bs4 import BeautifulSoup

import requests

URL = 'https://www.hola.com/horoscopo/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

titles = soup.select("h2.titulo")

for row in titles:
    print(row.get_text().strip())
