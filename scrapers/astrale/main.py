import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from src.constants.focuses import *
from src.constants.signs import *
from src.keys.db_mongo import mongo_connection
from src.utils.Mongo import Mongo
from src.utils.headless import *

# CONNECTION
mongo = Mongo(mongo_connection)

# BASICS
daily_data = []
parser = "lxml"

# DAY ---
day = datetime.today().strftime('%Y-%m-%d')
print('Day -- ' + day)

# SIGNS BASE ---
for sign in signs_en:
    daily_data.append({
        'day': day,
        'sign': sign,
        'contents': {
            'focus': '',
            'love':
                {'es': '', 'en': ''},
            'health':
                {'es': '', 'en': ''},
            'work':
                {'es': '', 'en': ''},
            'compatibility': [],
            'numbers': []
        }
    })

print("Signs done")

# LUCKY NUMBERS - COMPATIBILITY - FOCUS OF THE DAY
for data in daily_data:
    # NUMBERS
    for x in range(3):
        random_number = random.randrange(1, 100)
        while random_number in data['contents']['numbers']:
            random_number = random.randrange(1, 100)

        data['contents']['numbers'].append(
            random_number
        )
    # LOVE
    while len(data['contents']['compatibility']) < 2:
        random_sign = signs_en[random.randrange(0, len(signs_en) - 1)]
        if random_sign not in data['contents']['compatibility']:
            data['contents']['compatibility'].append(random_sign)
    # HATE
    data['contents']['focus'] = focuses[random.randrange(0, len(focuses) - 1)]

print("Numbers, compatibility and foucs done")

# SPANISH
# Get the latest blog entry for this blog ( 1 each day )
print("Spanish data in progress...")

spanish_base_url = 'https://www.semana.es/horoscopo/'
page = requests.get(spanish_base_url, headers={'User-Agent': random_user_agent()})
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

print("Spanish data done")

# ENGLISH
print("English data in progress...")

base = "https://www.prokerala.com"
english_base_url = "https://www.prokerala.com/astrology/horoscope/"
page = requests.get(english_base_url, headers={'User-Agent': random_user_agent()})
english_soup = BeautifulSoup(page.content, parser)
page_signs = english_soup.select('h2.sample-prediction-sign > a')
for data in daily_data:
    for page_sign in page_signs:
        if page_sign.text == data['sign']:
            url = base + page_sign.get('href')
            headless = chrome()
            headless.get(url)
            english_soup = BeautifulSoup(headless.page_source, parser)
            headless.quit()
            panels = english_soup.select('div.horoscope-panel')
            data['contents']['health']['en'] = panels[1].text.replace('\n', '').strip()
            data['contents']['love']['en'] = panels[2].text.replace('\n', '').replace(
                'Understand compatibility with  love horoscope', '').replace(
                'Check love percentage using love calculator.', '').strip()
            data['contents']['work']['en'] = panels[3].text.replace('\n', '').strip()

print("English data done")

print("Updating mongo...")

mongo.db.daily.insert_many(daily_data)

print("Everything done, see you tomorrow!")

exit(0)
