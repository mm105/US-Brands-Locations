import requests
import pandas as pd


zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

target_data = pd.DataFrame(columns=[
    'ID', 'Address', 'City', 'County', 'State', 'Latitude', 'Longitude', 'Zipcode'])


URL = "https://api.target.com/location_proximities/v1/nearby_locations"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        prms = {'limit': 20, 'unit': 'mile', 'within': 100, 'place': zipcode,
                'type': 'store', 'key': '8df66ea1e1fc070a6ea99e942431c9cd67a80f02'}
        res = requests.get(
            url=URL, params=prms)
        data = res.json()
        stores = data['locations']

        if len(stores) != 0:
            for store in range(len(stores)):
                ID = stores[store]['location_id']
                addr1 = stores[store]['address']['address_line1']
                addr2 = stores[store]['address']['address_line2']
                address = ''
                if addr1 != None:
                    address = address + addr1
                if addr2 != None:
                    address = address + addr2
                city = stores[store]['address']['city']
                county = stores[store]['address']['county']
                state = stores[store]['address']['region']
                latitude = stores[store]['geographic_specifications']['latitude']
                longitude = stores[store]['geographic_specifications']['longitude']

                if (ID in target_data['ID'].values):
                    continue
                else:
                    target_data = target_data.append(
                        {'ID': ID, 'Address': address, 'City': city, 'County': county, 'State': state, 'Latitude': latitude, 'Longitude': longitude, 'Zipcode': zipcode}, ignore_index=True)

finally:
    target_data.to_csv(r'D:\\...',
                       index=False, header=True)
