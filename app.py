from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import random
app = Flask(__name__)

@app.route("/")
def get_listings():
    url= "https://www.airbnb.it/s/Italia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-09-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Italia&place_id=ChIJA9KNRIL-1BIRb15jJFz1LOI&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
    response= requests.get(url)
    soup= BeautifulSoup(response.content, "lxml")
    listings_prices = {} #dizionario nome-prezzo
    listings_data = [] # lista di tuple (nome,link foto)
    for item in soup.select('[itemprop=itemListElement]'):   # nel sito di airbnb i div con itemprop="itemListElement" contengono tutti i dati necessari
            img= item.find("img", {"class":"itu7ddv i1mla2as i1cqnm0r dir dir-ltr"}) #ricerco l'elemento immagine con quella classe 
            foto = img['src'] #prendo il contenuto dell'attributo src quindi il link dell'immagaine 

            price= item.find("span",{"class":"a8jt5op dir dir-ltr"}).getText()[:13] #prendo il prezzo del listing , prendo solo i primi 13 caratteri che sarebbero XXX$ a notte 
            
            for name in item.select('[itemprop=name]'):     #ciclo tra tutti i nomi dei listing
                 listings_data.append((name['content'], foto)) # e appendo una tupla alla lista listings_data con (nome,link foto)
                 
                 listings_prices[name["content"]] = price.replace(u'\xa0', u' ').replace(",", "N/A")  #assegno il prezzo al nome della casa e rimpiazzo alcuni caratteri inutili

    


#randomizzazione    
    rand1 = random.randint(0, len(listings_data) - 1)
    titolo1 = listings_data[rand1][0]   # titolo è uguale al titolo della tupla di indice rand1
    foto1 = listings_data[rand1][1] # foto è uguale al link della foto della tupla di indicie rand 1
    prezzo1 = listings_prices[titolo1] # il prezzo è uguale al prezzo del listing che ha per nome titolo1

# PREVENZIONE DUPLICATI
    rand2 = random.randint(0, len(listings_data) - 1)
    while rand2 == rand1:
        rand2 = random.randint(0, len(listings_data) - 1) #rigenero un numero casuale se uguale all'altro 
    titolo2 = listings_data[rand2][0]
    foto2 = listings_data[rand2][1]
    prezzo2 = listings_prices[titolo2]

    rand3 = random.randint(0, len(listings_data) - 1)
    while rand3 == rand1 or rand3 == rand2: 
        rand3 = random.randint(0, len(listings_data) - 1)  #rigenero un numero casuale se uguale a un altro 
    titolo3 = listings_data[rand3][0]
    foto3 = listings_data[rand3][1]
    prezzo3 = listings_prices[titolo3]
     
# "esporto" i titoli , i link delle foto e i prezzi al template html 
    return render_template("index.html", titolo=titolo1 , foto=foto1, titolo2=titolo2 , foto2=foto2, titolo3=titolo3, foto3=foto3 , prezzo= prezzo1 , prezzo2=prezzo2, prezzo3 = prezzo3)
