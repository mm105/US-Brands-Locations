import requests
import pandas as pd

zipcode_data = pd.read_csv(
    'D:\\...',  dtype=str)

kroger_data = pd.DataFrame(columns=[
    'ID', 'Address', 'City', 'State', 'Latitude', 'Longitude', 'Zipcode'])


URL = "https://www.kroger.com/stores/api/graphql"

try:
    for index in range(len(zipcode_data)):
        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        query = {
            "query": "\n      query storeSearch($searchText: String!, $filters: [String]!) {\n        storeSearch(searchText: $searchText, filters: $filters) {\n          stores {\n            ...storeSearchResult\n          }\n          fuel {\n            ...storeSearchResult\n          }\n          shouldShowFuelMessage\n        }\n      }\n      \n  fragment storeSearchResult on Store {\n    banner\n    vanityName\n    divisionNumber\n    storeNumber\n    phoneNumber\n    showWeeklyAd\n    showShopThisStoreAndPreferredStoreButtons\n    storeType\n    distance\n    latitude\n    longitude\n    tz\n    ungroupedFormattedHours {\n      displayName\n      displayHours\n      isToday\n    }\n    address {\n      addressLine1\n      addressLine2\n      city\n      countryCode\n      stateCode\n      zip\n    }\n    pharmacy {\n      phoneNumber\n    }\n    departments {\n      code\n    }\n    fulfillmentMethods{\n      hasPickup\n      hasDelivery\n    }\n  }\n",
            "variables": {
                "searchText": zipcode,
                "filters": []
            },
            "operationName": "storeSearch"
        }
        l = len(str(query))
        headers = {'Content-Type': 'application/json',
                   'Accept': '*/*',
                   'Content-Length': str(l),
                   'Connection': 'keep-alive',
                   'User-Agent': "PostmanRuntime/7.26.10"}
        res = requests.post(
            url=URL, json=query, headers=headers)
        print(res)
        data = res.json()
        if data != None:
            stores = data['data']['storeSearch']['stores']

            if len(stores) != 0:
                for store in range(len(stores)):
                    ID = stores[store]['storeNumber']
                    addr1 = stores[store]['address']['addressLine1']
                    addr2 = stores[store]['address']['addressLine2']
                    city = stores[store]['address']['city']
                    state = stores[store]['address']['stateCode']
                    address = ''
                    if addr1 != None:
                        address = address + addr1
                    if addr2 != None:
                        address = address + addr2
                    latitude = stores[store]['latitude']
                    longitude = stores[store]['longitude']

                    if (ID in kroger_data['ID'].values):
                        continue
                    else:
                        kroger_data = kroger_data.append(
                            {'ID': ID, 'Address': address, 'City': city, 'State': state, 'Latitude': latitude, 'Longitude': longitude, 'Zipcode': zipcode}, ignore_index=True)

finally:
    kroger_data.to_csv(r'D:\\...',
                       index=False, header=True)
