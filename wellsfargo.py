import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

wellsfargo_data = pd.DataFrame(columns=[
    'Address', 'City', 'State', 'Postal_code',  'Zipcode_testing(dont use this)'])


URL = "https://www.wellsfargo.com/locator/search/"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']

        res = requests.get(
            url=URL, params={'searchTxt': zipcode})
        page = res.text
        page = bs(page, 'html.parser')

        resultList = page.find('ul', {'id': 'searchResultsList'})
        li = len(page.find_all('li', {'class': "aResult"}))

        for index in range(li):
            store = page.find('li', {'id': 'result' + str(index + 1)})
            address = store.find('div', {'data-address': "address"}).string
            city = store.find('span', {'itemprop': "addressLocality"}).string
            state = store.find('abbr', {'class': "region"}).string
            postal_code = store.find('span', {'class': 'postal-code'}).string

            if (address in wellsfargo_data['Address']. values):
                continue
            else:
                wellsfargo_data = wellsfargo_data.append(
                    {'Address': address, 'City': city, 'State': state, 'Postal_code': postal_code,  'Zipcode_testing(dont use this)': zipcode}, ignore_index=True)

finally:
    wellsfargo_data.to_csv(r'D:\\...',
                           index=False, header=True)
