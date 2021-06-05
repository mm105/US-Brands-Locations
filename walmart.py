import requests
import pandas as pd


zipcode_data = pd.read_csv(
    'D:\\...', usecols=['ZIP_CODE', 'STATE'], dtype=str)

walmart_data = pd.DataFrame(
    columns=['ID', 'Display_Name', 'Type_name', 'Type_display_name', 'Postal_code', 'Address', 'Latitude', 'Longitude', 'City', 'State', 'Phone', 'Zip_code'])


URL = "https://www.walmart.com/store/finder/electrode/api/stores"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        res = requests.get(
            url=URL, params={'singleLineAddr': zipcode, 'distance': 50})
        data = res.json()
        stores = data['payload']['storesData']['stores']

        if len(stores) != 0:
            for store in range(len(stores)):
                ID = stores[store]['id']
                display_name = stores[store]['displayName']
                type_name = stores[store]['storeType']['name']
                type_display_name = stores[store]['storeType']['displayName']
                postal_code = stores[store]['address']['postalCode']
                address = stores[store]['address']['address']
                lat = stores[store]['geoPoint']['latitude']
                lng = stores[store]['geoPoint']['longitude']
                city = stores[store]['address']['city']
                state = stores[store]['address']['state']
                phone = stores[store]['phone']

                if (ID in walmart_data['ID'].values):
                    continue
                else:
                    walmart_data = walmart_data.append({'ID': ID, 'Display_Name': display_name, 'Type_name': type_name, 'Type_display_name': type_display_name,
                                                        'Postal_code': postal_code, 'Address': address, 'Latitude': lat, 'Longitude': lng, 'City': city, 'State': state, 'Phone': phone, 'Zip_code': zipcode}, ignore_index=True)

finally:
    walmart_data.to_csv(r'D:\\...',
                        index=False, header=True)
