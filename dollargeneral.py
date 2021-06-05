import requests
import pandas as pd


zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

dollargeneral_data = pd.DataFrame(columns=[
                                  'ID', 'Address', 'City', 'State', 'Phone', 'Latitude', 'Longitude', 'Zipcode'])


URL = "https://www.dollargeneral.com/commerce/store/locator/latlon"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        lng = float(zipcode_data.iloc[index]['LNG'])
        lat = float(zipcode_data.iloc[index]['LAT'])
        res = requests.get(
            url=URL, params={'longitude': lng, 'latitude': lat, 'radius': 15})
        stores = res.json()

        if len(stores) != 0:
            for store in range(len(stores)):
                ID = stores[store]['storenumber']
                address = stores[store]['address']
                city = stores[store]['city']
                state = stores[store]['state']
                phone = stores[store]['phone']
                latitude = stores[store]['lat']
                longitude = stores[store]['lon']
                if (ID in dollargeneral_data['ID'].values):
                    continue
                else:
                    dollargeneral_data = dollargeneral_data.append(
                        {'ID': ID, 'Address': address, 'City': city, 'State': state, 'Phone': phone, 'Latitude': latitude, 'Longitude': longitude, 'Zipcode': zipcode}, ignore_index=True)

finally:
    dollargeneral_data.to_csv(r'D:\\...',
                              index=False, header=True)
