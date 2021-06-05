import requests
import pandas as pd
import json
from bs4 import BeautifulSoup as bs

zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

aldi_data = pd.DataFrame(columns=[
    'ID', 'Address', 'Longitude', 'Latitude', 'City', 'State', 'Postal',  'Zipcode_testing(dont use this)'])


URL = "https://www.aldi.us/stores/en-us/Search"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']

        res = requests.get(
            url=URL, params={'SingleSlotGeo': zipcode})
        page = res.text
        page = bs(page, 'html.parser')

        resultList = page.find('ul', {'id': 'resultList'})
        if resultList is not None:
            stores = resultList.find_all('li')

            for elem in stores:
                data = json.loads(elem.get('data-json'))
                ID = data['id']
                longitude = data['locX']
                latitude = data['locY']
                address = elem.find(
                    'div', {'itemprop': 'streetAddress'}).string
                loc = str(elem.find(
                    'div', {'itemprop': 'addressLocality'}).string)
                city = loc.split(',')[0]
                state = loc.split(',')[1].split(' ')[1]
                postal = loc.split(',')[1].split(' ')[2]
                if (address in aldi_data['Address']. values):
                    continue
                else:
                    aldi_data = aldi_data.append(
                        {'ID': ID, 'Address': address, 'Longitude': longitude, 'Latitude': latitude, 'City': city, 'State': state, 'Postal': postal, 'Zipcode_testing(dont use this)': zipcode}, ignore_index=True)


finally:
    aldi_data.to_csv(r'D:\\...',
                     index=False, header=True)
