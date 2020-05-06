import requests
from pprint import pprint
from bs4 import BeautifulSoup
from src.utils.Mongo import Mongo
from src.keys.db_mongo import mongo_connection
from datetime import datetime
from src.constants.signs import *

mongo = Mongo(mongo_connection)
arrayDailyData = []

# DAY ---
day = datetime.today().strftime('%Y-%m-%d')

# SIGNS BASE ---
for sign in signs_en:
    arrayDailyData.append({
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
spanishBaseUrl = 'https://www.semana.es/horoscopo/'
page = requests.get(spanishBaseUrl)
spanishSoup = BeautifulSoup(page.content, "html.parser")
days = spanishSoup.select("div.td_module_10:first-child a:first-child")
dayUrl = days[0].get('href')

spanishDayUrl = dayUrl
page = requests.get(spanishDayUrl)
spanishSoup = BeautifulSoup(page.content, "html.parser")
spanishSigns = spanishSoup.select("div.td-post-content h3")

# We get love, work and health texts for spanish here
for dailyData in arrayDailyData:
    spSign = signs_en_to_es[dailyData['sign']]
    for pageSign in spanishSigns:
        if pageSign.text == spSign:
            sections = pageSign.parent.select('p > strong')
            dailyData['contents']['health']['es'] = pageSign.find_next_sibling('p').text.replace('Salud:', '').strip()
            dailyData['contents']['love']['es'] = pageSign.find_next_sibling('p').find_next_sibling('p').text.replace(
                'Amor:', '').strip()
            dailyData['contents']['work']['es'] = pageSign.find_next_sibling('p').find_next_sibling(
                'p').find_next_sibling('p').text \
                .replace('Ver más sobre ' + spSign + '…', '') \
                .replace('Dinero y trabajo:', '') \
                .strip()

# ENGLISH
# @todo
