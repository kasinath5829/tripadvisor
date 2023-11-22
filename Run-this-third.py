from bs4 import BeautifulSoup
import requests
import time
import re
import pymongo
import json

# Initialize MongoDB client and database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydb"]
mycol = mydb["hotels_prices"]

# Set User-Agent header for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'
}

# Function to scrape hotel data
def scrape_hotel_data(url):
    try:
        res = requests.get(url, headers=headers)
        time.sleep(1)
        doc = BeautifulSoup(res.content, 'html.parser')
        time.sleep(1)
        json_object = json.loads(str(doc))

        hotel_url = json_object['result']['hotel_url'][0]
        print("Hotel URL:", hotel_url)

        rates_expedia = next((rate['rate'] for rate in json_object['result']['rates'] if rate['name'] == 'Expedia'), None)
        print("Expedia Rate:", rates_expedia)

        rates_bookings = next((rate['rate'] for rate in json_object['result']['rates'] if rate['name'] == 'Booking.com'), None)
        print("Booking.com Rate:", rates_bookings)

        rates_hotel_com = next((rate['rate'] for rate in json_object['result']['rates'] if rate['name'] == 'Hotels.com'), None)
        print("Hotels.com Rate:", rates_hotel_com)

        rates_agoda_com = next((rate['rate'] for rate in json_object['result']['rates'] if rate['name'] == 'Agoda.com'), None)
        print("Agoda.com Rate:", rates_agoda_com)
        
    except:
        url = 'https://www.tripadvisor.com/Hotel_Review-' + str(hotel_keys)
        res = requests.get(url, headers=headers)
        time.sleep(3)
        tripadvisor = BeautifulSoup(res.content, 'html.parser')

        try:
            expedia = tripadvisor.find("img", {'alt': 'Expedia.com'}).parent.nextSibling
            rates_expedia = expedia.find('div', {'class': 'vyNCd b Wi'}).text
        except:
            rates_expedia = None
        print("Expedia Rate:", rates_expedia)

        try:
            booking = tripadvisor.find("img", {'alt': 'Booking.com'}).parent.nextSibling
            rates_bookings = booking.find('div', {'class': 'vyNCd b Wi'}).text
        except:
            rates_bookings = None
        print("Booking.com Rate:", rates_bookings)

        try:
            hotel = tripadvisor.find("img", {'alt': 'Hotels.com'}).parent.nextSibling
            rates_hotel_com = hotel.find('div', {'class': 'vyNCd b Wi'}).text
        except:
            rates_hotel_com = None
        print("Hotels.com Rate:", rates_hotel_com)

        try:
            agoda = tripadvisor.find("img", {'alt': 'Agoda.com'}).parent.nextSibling
            rates_agoda_com = agoda.find('div', {'class': 'vyNCd b Wi'}).text
        except:
            rates_agoda_com = None
        print("Agoda.com Rate:", rates_agoda_com)
        hotel_url = url

    return {
        'Hotel Name': hotel_name,
        'Expedia Rate': rates_expedia,
        'Booking.com Rate': rates_bookings,
        'Hotels.com Rate': rates_hotel_com,
        'Agoda.com Rate': rates_agoda_com,
        'Hotel URL': hotel_url
    }

# Loop through the search result pages
for i in range(2, 15):
    # Open the saved HTML file for scraping
    with open(f"trip_advisor_search_pg{i}.html", "r", encoding="utf-8") as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        divs = soup.find_all("div", {'class': 'listing_title'})

        for div in divs:
            hotel_name = div.a.text
            href = div.a.get('href')
            hotel_keys = re.findall('g[0-9]*-d[0-9]*', str(href))[0]
            hotel_data = scrape_hotel_data(f'https://data.xotelo.com/api/rates?hotel_key={hotel_keys}&chk_in=2022-05-28&chk_out=2022-05-30')

            try:
                mycol.insert_one(hotel_data)
            except:
                continue
            time.sleep(3)

# Retrieve and update additional information for the initial database
docs = mycol.find({"Address": {"$exists": True}}, {"_id": 1, "Hotel URL": 1})
i = 1

for doc in docs:
    url = doc['Hotel URL']
    obid = doc['_id']

    print(i)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    city = re.compile(r'San Francisco, CA')
    address = soup.find("span", text=city).text
    print("Address:", address)

    try:
        phone = soup.find("span", {'class': 'eeFQx ceIOZ yYjkv'}).text
        print("Phone:", phone)
    except:
        phone = ""

    try:
        reviews = soup.find("span", {'class': 'btQSs q Wi z Wc'}).text
        print("Number of Reviews:", reviews)
    except:
        reviews = "0 reviews"

    try:
        pattern = re.compile(r'for walkers')
        walkingscore = soup.find("span", text=pattern).parent.previousSibling.text
        print("Great for Walkers Score:", walkingscore)
    except:
        try:
            pattern = re.compile(r'Somewhat walkable')
            walkingscore = soup.find("span", text=pattern).parent.previousSibling.text
        except:
            walkingscore = "No Score Available"

    try:
        pattern2 = re.compile(r'Restaurants')
        restaurantscore = soup.find("span", text=pattern2).parent.previousSibling.text
        print("Restaurant Score:", restaurantscore)
    except:
        restaurantscore = "No Score Available"

    try:
        pattern3 = re.compile(r'Attractions')
        attractionscore = soup.find("span", text=pattern3).parent.previousSibling.text
        print("Attractions Score:", attractionscore)
    except:
        attractionscore = "No Score Available"

    mycol.find_one_and_update({'_id': obid}, {"$set": {'Address': address}})
    mycol.find_one_and_update({'_id': obid}, {"$set": {'Phone': phone}})
    mycol.find_one_and_update({'_id': obid}, {"$set": {'Number of Reviews': reviews}})
    mycol.find_one_and_update({'_id': obid}, {"$set": {'Great for Walkers Score': walkingscore}})
    mycol.find_one_and_update({'_id': obid}, {"$set": {'Restaurant Score': restaurantscore}})
    mycol.find_one_and_update({'_id': obid}, {"$set": {'Attractions Score': attractionscore}})

    time.sleep(3)
    i += 1
