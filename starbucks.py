import requests
import pandas as pd


zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

starbucks_data = pd.DataFrame(
    columns=['ID', 'Name', 'Latitude', 'Longitude', 'Address', 'City', 'State', 'Zip'])


URL = "https://app.starbucks.com/bff/locations"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        lat = zipcode_data.iloc[index]['LAT']
        lng = zipcode_data.iloc[index]['LNG']
        req = requests.get(
            url=URL, params={'lng': lng, 'lat': lat}, headers={'X-Requested-With': 'XMLHttpRequest'})
        data = req.json()
        stores = data['stores']

        if len(stores) != 0:
            for store in range(len(stores)):

                ID = stores[store]['id']
                name = stores[store]['name']
                latitude = stores[store]['coordinates']['latitude']
                longitude = stores[store]['coordinates']['longitude']
                addr1 = stores[store]['address']['streetAddressLine1']
                addr2 = stores[store]['address']['streetAddressLine2']
                addr3 = stores[store]['address']['streetAddressLine3']
                address = ''
                if addr1 != None:
                    address = address + addr1
                if addr2 != None:
                    address = address + addr2
                if addr3 != None:
                    address = address + addr3
                city = stores[store]['address']['city']
                state = stores[store]['address']['countrySubdivisionCode']

                if (ID in starbucks_data['ID'].values):
                    continue
                else:
                    starbucks_data = starbucks_data.append({'ID': ID, 'Name': name, 'Latitude': latitude, 'Longitude': longitude,
                                                            'Address': address, 'City': city, 'State': state, 'Zip': zipcode}, ignore_index=True)

finally:
    starbucks_data.to_csv(r'D:\\...',
                          index=False, header=True)
