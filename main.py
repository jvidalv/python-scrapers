import requests
from pprint import pprint
from bs4 import BeautifulSoup
from src.utils.Mongo import Mongo
from src.keys.db_mongo import mongo_connection
from datetime import datetime
from src.constants.signs import *
from src.utils.headless import *
import time

# CONNECTION
mongo = Mongo(mongo_connection)

# BASICS
daily_data = []
parser = "lxml"

# DAY ---
day = datetime.today().strftime('%Y-%m-%d')

# SIGNS BASE ---
for sign in signs_en:
    daily_data.append({
        'day': day,
        'sign': sign,
        'contents': {
            'love':
                {'es': '', 'en': ''},
            'health':
                {'es': '', 'en': ''},
            'work':
                {'es': '', 'en': ''},
            'you_hate': [],
            'you_love': [],
            'numbers': []
        }
    })

# SPANISH
# Get the latest blog entry for this blog ( 1 each day )
spanish_base_url = 'https://www.semana.es/horoscopo/'
page = requests.get(spanish_base_url)
spanish_soup = BeautifulSoup(page.content, parser)
days = spanish_soup.select("div.td_module_10:first-child a:first-child")
day_url = days[0].get('href')
spanish_day_url = day_url
page = requests.get(spanish_day_url)
spanish_soup = BeautifulSoup(page.content, parser)
spanish_signs = spanish_soup.select("div.td-post-content h3")

# We get love, work and health texts for spanish here
for data in daily_data:
    sp_sign = signs_en_to_es[data['sign']]
    for page_sign in spanish_signs:
        if page_sign.text == sp_sign:
            p_data = page_sign.parent.select('p')
            data['contents']['health']['es'] = p_data[2].text.lstrip('Salud:').strip()
            data['contents']['love']['es'] = p_data[3].text.lstrip('Amor:').strip()
            data['contents']['work']['es'] = p_data[4].text.lstrip('Dinero y trabajo:').split('Ver más sobre')[
                0].strip()

# ENGLISH
base = "https://www.prokerala.com"
english_base_url = "https://www.prokerala.com/astrology/horoscope/"
page = requests.get(english_base_url)
english_soup = BeautifulSoup(page.content, parser)
page_signs = english_soup.select('h2.sample-prediction-sign > a')
for data in daily_data:
    for page_sign in page_signs:
        if page_sign.text == data['sign']:
            headless = chrome()
            headless.get(base + page_sign.get('href'))
            english_soup = BeautifulSoup(headless.page_source, parser)
            panels = english_soup.select('div.horoscope-panel')
            data['contents']['health']['en'] = panels[1].text.replace('\n', '').strip()
            data['contents']['love']['en'] = panels[2].text.replace('\n', '').replace(
                'Understand compatibility with  love horoscope', '').replace(
                'Check love percentage using love calculator.', '').strip()
            data['contents']['work']['en'] = panels[3].text.replace('\n', '').strip()

pprint(daily_data)

# @todo
