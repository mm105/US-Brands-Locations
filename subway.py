import requests
import pandas as pd
import json


zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

subway_data = pd.DataFrame(
    columns=['ID', 'Address', 'City', 'State', 'Latitude', 'Longitude', 'Zipcode'])


URL = "https://locator-svc.subway.com/v3/GetLocations.ashx"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        lat = zipcode_data.iloc[index]['LAT']
        lng = zipcode_data.iloc[index]['LNG']

        q = {"InputText": "", "GeoCode": {"name": "99901", "Latitude": lat, "Longitude": lng, "CountryCode": "US", "PostalCode": ""},
             "DetectedLocation": {"Latitude": 0, "Longitude": 0, "Accuracy": 0}, "Paging": {"StartIndex": 1, "PageSize": 30},
             "ConsumerParameters": {"metric": False, "culture": "en-US", "country": "US", "size": "M", "template": "", "rtl": False, "clientId": "17", "key": "SUBWAY_PROD"},
             "Filters": [], "LocationType": 1, "behavior": "", "FavoriteStores": None, "RecentStores": None,
             "Stats": {"abc": [{"N": "geo", "R": "A"}], "src": "page", "act": "page", "c": "subwayLocator"}}

        query = json.dumps(q)
        res = requests.get(url=URL, params={'q': query})
        data = res.text
        data = data[1:-1]
        data = json.loads(data)
        stores = data['ResultData']

        # print((stores))
        if len(stores) != 0:
            for store in range(len(stores)):
                ID = stores[store]['LocationId']['StoreNumber']
                addr1 = stores[store]['Address']['Address1']
                addr2 = stores[store]['Address']['Address2']
                addr3 = stores[store]['Address']['Address3']
                address = addr1 + addr2 + addr3
                city = stores[store]['Address']['City']
                state = stores[store]['Address']['StateProvCode']
                latitude = stores[store]['Geo']['Latitude']
                longitude = stores[store]['Geo']['Longitude']

                if (ID in subway_data['ID'].values):
                    continue
                else:
                    subway_data = subway_data.append({'ID': ID, 'Address': address, 'City': city,
                                                      'State': state, 'Latitude': latitude, 'Longitude': longitude, 'Zipcode': zipcode}, ignore_index=True)

finally:
    subway_data.to_csv(r'D:\\...',
                       index=False, header=True)
