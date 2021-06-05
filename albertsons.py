import requests
import pandas as pd


zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

albertson_data = pd.DataFrame(columns=[
    'ID', 'Address', 'City', 'State', 'Latitude', 'Longitude', 'Zipcode'])


URL = "https://local.albertsons.com/locator"

try:
    for index in range(len(zipcode_data)):

        zipcode = zipcode_data.iloc[index]['ZIP_CODE']

        res = requests.get(
            url=URL, params={'q': zipcode}, headers={'Accept': 'application/json'})
        data = res.json()
        stores = data['response']['entities']

        if len(stores) != 0:
            for store in range(len(stores)):
                ID = stores[store]['distance']['id']
                addr1 = stores[store]['profile']['address']['line1']
                addr2 = stores[store]['profile']['address']['line2']
                addr3 = stores[store]['profile']['address']['line3']
                address = ''
                if addr1 != None:
                    address = address + addr1
                if addr2 != None:
                    address = address + addr2
                if addr3 != None:
                    address = address + addr3
                city = stores[store]['profile']['address']['city']
                state = stores[store]['profile']['address']['region']
                try:
                    latitude = stores[store]['profile']['geocodedCoordinate']['lat']
                    longitude = stores[store]['profile']['geocodedCoordinate']['long']
                except:
                    latitude = None
                    longitude = None

                if (ID in albertson_data['ID'].values):
                    continue
                else:
                    albertson_data = albertson_data.append(
                        {'ID': ID, 'Address': address, 'City': city, 'State': state, 'Latitude': latitude, 'Longitude': longitude, 'Zipcode': zipcode}, ignore_index=True)

finally:
    albertson_data.to_csv(r'D:\\...',
                          index=False, header=True)
