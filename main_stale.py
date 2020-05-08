import requests
import random
from pprint import pprint
from bs4 import BeautifulSoup
from src.utils.Mongo import Mongo
from src.keys.db_mongo import mongo_connection
from datetime import datetime
from src.constants.signs import *
from src.utils.headless import *

# CONNECTION
mongo = Mongo(mongo_connection)

# BASICS
stale_data = []
parser = "lxml"

# STALE DATA BASE
for sign1 in signs_en:
    for sign2 in signs_en:
        stale_data.append({
            'type': 'compatibility',
            'sign1': sign1,
            'sign2': sign2,
            'resume': {
                'en': '',
                'es': ''
            },
            'relationship': {
                'en': '',
                'es': ''
            },
            'percents': {
                'intimate': random.randrange(30, 100),
                'mindset': random.randrange(30, 100),
                'feelings': random.randrange(30, 100),
                'priorities': random.randrange(30, 100),
                'interests': random.randrange(30, 100),
                'sport': random.randrange(30, 100),
            }
        })

# ENGLISH
for data in stale_data:
    sign1 = data['sign1'].lower()
    url_base = "https://askastrology.com/zodiac-compatibility/" + sign1 + "-compatibility/" + sign1
    for data2 in stale_data:
        url_with_sign = url_base + '-' + data2['sign2'].lower()
        page = requests.get(url_with_sign, headers={'User-Agent': random_user_agent()})
        soup = BeautifulSoup(page.content, parser)
        compatibility_ps = soup.select('div.entry-content > p')
        data['resume']['en'] = compatibility_ps[0].text
        data['relationship']['en'] = compatibility_ps[1].text
        pprint(data)

# SPANISH
# todo
