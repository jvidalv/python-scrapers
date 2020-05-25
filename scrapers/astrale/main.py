import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from src.constants.focuses import *
from src.constants.signs import *
from src.keys.db_mongo import mongo_connection
from src.utils.Mongo import Mongo
from src.utils.headless import *
from src.utils.unicode import *

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
            'percents': {
                'love': random.randrange(30, 100),
                'work': random.randrange(30, 100),
                'health': random.randrange(30, 100)
            },
            'text':
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
    # COMPATIBILITY
    while len(data['contents']['compatibility']) < 3:
        random_sign = signs_en[random.randrange(0, len(signs_en) - 1)]
        if random_sign not in data['contents']['compatibility']:
            data['contents']['compatibility'].append(random_sign)
    # FOCUSES
    data['contents']['focus'] = focuses[random.randrange(0, len(focuses) - 1)]

print("Numbers, compatibility and focus done")

# SPANISH
print("Spanish data in progress...")

for data in daily_data:
    sp_sign = signs_en_to_es[data['sign']]
    spanish_base_url = 'https://www.hola.com/horoscopo/' + delete_accents(sp_sign.lower())
    page = requests.get(spanish_base_url, headers={'User-Agent': random_user_agent()})
    spanish_soup = BeautifulSoup(page.content, parser)
    ps = spanish_soup.select("div#resultados > *")
    data['contents']['text']['es'] = ps[2].text

print("Spanish data done")

# ENGLISH
print("English data in progress...")

base = "https://www.astrology-zodiac-signs.com/horoscope/"

for data in daily_data:
    page = requests.get(base + data['sign'].lower() + '/daily/', headers={'User-Agent': random_user_agent()})
    english_soup = BeautifulSoup(page.content, parser)
    ps = english_soup.select('div.dailyHoroscope > *')
    data['contents']['text']['en'] = ps[2].text + '\n' + ps[3].text

print("English data done")

print("Updating mongo...")

mongo.db.daily.insert_many(daily_data)

print("Everything done, see you tomorrow!")

exit(0)
