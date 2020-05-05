from pprint import pprint
from pymongo import MongoClient
from src.utils.Mongo import Mongo
from src.keys.db_mongo import mongo_connection

mongo = Mongo(mongo_connection)
serverStatusResult = mongo.db.users.find()

pprint(serverStatusResult)
# URL = 'https://www.hola.com/horoscopo/'
# page = requests.get(URL)
#
# soup = BeautifulSoup(page.content, "html.parser")
#
# titles = soup.select("h2.titulo")
#
# for row in titles:
#     print(row.get_text().strip())
