import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

#DATABASE - Google Firestore cloud----------------------------
db = firestore.client()
#CLASS---------------------------------------------------
class ads:

    def __init__(self, link_ML, link_SM, collection, p_limit, p_limit_boxed, all_keywords):
        self.link_ML = link_ML
        self.link_SM = link_SM
        self.collection = collection
        self.p_limit = p_limit
        self.p_limit_boxed = p_limit_boxed
        self.all_keywords = all_keywords

gb = ads('https://videojuegos.mercadolibre.com.mx/consolas/usado/gameboy', 'https://www.segundamano.mx/anuncios/mexico?q=game%20boy&pagina=', db.collection('gameboy'), 601, 1201, ["game", "boy", "gameboy"])
sega = ads('https://videojuegos.mercadolibre.com.mx/consolas/game-gear/usado/gamegear', 'https://www.segundamano.mx/anuncios/mexico?q=game%20gear&pagina=', db.collection('gamegear'), 801, 1801, ["gear", "game", "gamegear", "sega"])
neo = ads('https://videojuegos.mercadolibre.com.mx/consolas/usado/neo-geo-pocket', 'https://www.segundamano.mx/anuncios/mexico?q=neo%20geo%20pocket&pagina=', db.collection('neogeo'), 801, 1501, ["neo", "geo", "pocket", "ngpc", "neogeo"])
mini = ads('https://videojuegos.mercadolibre.com.mx/consolas/usado/mini', 'https://www.segundamano.mx/anuncios/mexico?q=nes%20mini&pagina=', db.collection('miniconsoles'),1501, 1501, ["classic", "nes", "snes", "turbografx", "neogeo", "super", "súper"])
games = ads('https://videojuegos.mercadolibre.com.mx/videojuegos/usado/gameboy', 'https://www.segundamano.mx/anuncios/mexico?q=gameboy&pagina=', db.collection('games'), 501, 1001, ["mario land", "wario land", "donkey", "spiderman", "battleships", "dr mario", "kirby", "popeye", "qix", "tennis", "zelda", "pokemon", "metroid", "f1", "kururin"])

pages = range(1, 2851, 50)
html_text =""
banned_keywords = ["repro", "re-pro", "repr0", "re-pr0", "re pro", "re pr0", "re_pro", "re_pr0", "generico", "génerico", "re_ pro", "re_ pr0", "carcasa"]

#LINKS TO GO THROUGH SM--------------------------------------------
pages_sm = range(1, 8)

PATH ="C:\Program Files (x86)\chromedriver.exe"

#REMOVE SOLD ITEMS------------------------------------------------
def remove_sold(coll):
    links_if_sold = []
    links_sold = []
    docs = coll.stream();
    for doc in docs:
        html_text = requests.get(doc.to_dict()['link']).text
        #if keywords found in each link's html text then delete the document from firestore by its ID
        if "Publicación finalizada" in html_text or "Publicación pausada" in html_text or "Ver artículo finalizado." in html_text or "RECOMENDADO" in html_text:
            key = doc.id
            coll.document(key).delete()
            print(f'I deleted a document')

#FIND STUFF ON MERCADOLIBRE-------------------------------------
def find_stuff_ML(website_link, collection, price_limit, price_limit_boxed, all_keywords):
    #for loop to go through all the pages using range, every pages' number has +50, hence 50 step each time = +1 page
    for n in pages:
        #URL - pages on Mercadolibre works like "desde_1" then "desde_51" etc
        html_text = requests.get(f'{website_link}_Desde_{n}').text
        #it only runs if the link is valid, ergo when there's no more pages it stops executing
        if "No hay publicaciones" in html_text:
            break
        else:
            soup = BeautifulSoup(html_text, 'lxml')
            #find products by class
            products = soup.find_all('div', class_='ui-search-result__wrapper')
            for index, product in enumerate(products):
                product_name = product.h2.text.lower() #title of ad
                product_id = product.find('input', {'name': 'itemId'}).get('value') #they only have special ID in one of the input tags
                product_link = product.a['href']
                needed_keywords = any(all_keyword in product_name for all_keyword in all_keywords)
                if needed_keywords is True:
                    product_price = int(product.find('span', class_='price-tag-fraction').text.replace(',', ''))
                    product_details = {'name': product_name, 'price': product_price, 'link': product_link, 'product id': product_id}
                    if 'caja' in product_name and product_price < price_limit_boxed or product_price < price_limit:
                        filter_keywords = any(banned_keyword in product_name for banned_keyword in banned_keywords)
                        if filter_keywords is False:
                            #set updates/overwrites the doc if already exists
                            result = collection.document(product_id).set(product_details)
                            print(f'{product_name} saved from ML')
                else:
                    print('Not needed')

#FIND STUFF ON SEGUNDAMANO-------------------------------------
def find_stuff_SM(website_link, collection, price_limit, price_limit_boxed, all_keywords):
    #for loop to go through all the pages using range, every pages' number has +50, hence 50 step each time = +1 page
    driver = webdriver.Chrome(PATH)
    for n in pages_sm:
        driver.get(f'{website_link}{n}')
        #URL - pages on Mercadolibre works like "desde_1" then "desde_51" etc
        html_text = driver.execute_script("return document.documentElement.innerHTML;")
        soup = BeautifulSoup(html_text, 'lxml')
        #find products by class
        products = soup.find_all('a', class_='card-container')
        for index, product in enumerate(products):
            product_name = product.find('p', class_='card-data-title grid-data-title').text.lower() #title of ad
            product_link = product['href']
            product_id = product_link[-9:]
            product_date = product.find('p', class_='card-data-bottom-published').text.lower()
            needed_keywords = any(all_keyword in product_name for all_keyword in all_keywords)
            if '2020' not in product_date:
                if needed_keywords is True:
                    product_price = int(product.find('p', class_='card-data-bottom-container-price').text.replace(',', '').replace('$', ''))
                    product_details = {'name': product_name, 'price': product_price, 'link': product_link, 'product id': product_id}
                    if 'caja' in product_name and product_price < price_limit_boxed or product_price < price_limit:
                        filter_keywords = any(banned_keyword in product_name for banned_keyword in banned_keywords)
                        if filter_keywords is False:
                            #set updates/overwrites the doc if already exists
                            result = collection.document(product_id).set(product_details)
                            print(f'{product_name} saved from Segundamano')
                else:
                    print('Not needed')

#ALL TOGETHER
def find_stuff_also_delete():
    find_stuff_ML(gb.link_ML, gb.collection, gb.p_limit, gb.p_limit_boxed, gb.all_keywords)
    find_stuff_ML(sega.link_ML, sega.collection, sega.p_limit, sega.p_limit_boxed, sega.all_keywords)
    find_stuff_ML(games.link_ML, games.collection, games.p_limit, games.p_limit_boxed, games.all_keywords)
    find_stuff_ML(neo.link_ML, neo.collection, neo.p_limit, neo.p_limit_boxed, neo.all_keywords)
    find_stuff_ML(mini.link_ML, mini.collection, mini.p_limit, mini.p_limit_boxed, mini.all_keywords)
    find_stuff_SM(gb.link_SM, gb.collection, gb.p_limit, gb.p_limit_boxed, gb.all_keywords)
    find_stuff_SM(sega.link_SM, sega.collection, sega.p_limit, sega.p_limit_boxed, sega.all_keywords)
    find_stuff_SM(games.link_SM, games.collection, games.p_limit, games.p_limit_boxed, games.all_keywords)
    find_stuff_SM(neo.link_SM, neo.collection, neo.p_limit, neo.p_limit_boxed, neo.all_keywords)
    find_stuff_SM(mini.link_SM, mini.collection, mini.p_limit, mini.p_limit_boxed, mini.all_keywords)
    print("Gonna delete now")
    remove_sold(gb.collection)
    remove_sold(sega.collection)
    remove_sold(games.collection)
    remove_sold(neo.collection)
    remove_sold(mini.collection)

#CALL
if __name__ == '__main__':
    while True:
        find_stuff_also_delete()
        print("I'm done, waiting 30 mins to rerun...")
        time_wait = 60 #in seconds therefore 1min
        time.sleep(time_wait * 30)
