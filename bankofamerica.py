import requests
import pandas as pd
import json


zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

bankofamerica_data = pd.DataFrame(columns=[
    'ID', 'Name', 'Address', 'City', 'State', 'Latitude', 'Longitude', 'Zipcode'])


URL = "https://maps.bankofamerica.com/api/getAsyncLocations"

try:
    for index in range(len(zipcode_data)):

        zipcode = zipcode_data.iloc[index]['ZIP_CODE']

        prms = {'template': 'search', 'level': 'search', 'search': zipcode}
        res = requests.get(
            url=URL, params=prms)
        data = res.json()
        stores = data['markers']

        if stores != None:
            for store in range(len(stores)):
                ID = stores[store]['locationId']
                latitude = stores[store]['lat']
                longitude = stores[store]['lng']
                info = stores[store]['info'][26:-6]
                info = json.loads(info)
                address = info['address_1'] + info['address_2']
                city = info['city']
                state = info['region']
                name = info['location_name']

                if (ID in bankofamerica_data['ID'].values):
                    continue
                else:
                    bankofamerica_data = bankofamerica_data.append(
                        {'ID': ID, 'Name': name, 'Address': address, 'City': city, 'State': state, 'Latitude': latitude, 'Longitude': longitude, 'Zipcode': zipcode}, ignore_index=True)

finally:
    bankofamerica_data.to_csv(r'D:\\Desktop\\...',
                              index=False, header=True)
