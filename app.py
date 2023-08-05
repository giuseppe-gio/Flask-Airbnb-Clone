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

    listings_data = []
    for item in soup.select('[itemprop=itemListElement]'):
            img= item.find("img", {"class":"itu7ddv i1mla2as i1cqnm0r dir dir-ltr"})
            foto = img['src']
            
            for name in item.select('[itemprop=name]'):
                 listings_data.append((name['content'], foto)) 
    print(listings_data)


    
    rand1 = random.randint(0, len(listings_data) - 1)
    titolo1 = listings_data[rand1][0]
    foto1 = listings_data[rand1][1]

    rand2 = random.randint(0, len(listings_data) - 1)
    while rand2 == rand1:
        rand2 = random.randint(0, len(listings_data) - 1)
    titolo2 = listings_data[rand2][0]
    foto2 = listings_data[rand2][1]

    rand3 = random.randint(0, len(listings_data) - 1)
    while rand3 == rand1 or rand3 == rand2:
        rand3 = random.randint(0, len(listings_data) - 1)
    titolo3 = listings_data[rand3][0]
    foto3 = listings_data[rand3][1]
     

    return render_template("index.html", titolo=titolo1 , foto=foto1, titolo2=titolo2 , foto2=foto2, titolo3=titolo3, foto3=foto3)
