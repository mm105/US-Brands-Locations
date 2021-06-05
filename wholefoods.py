from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import pandas as pd
import time
import sys
import os

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(
    executable_path="C:\\Users\\datasoft\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe", options=options)
driver.get('https://www.wholefoodsmarket.com/stores')
driver.maximize_window()

zipcode_data = pd.read_csv(
    'C:\\...',  dtype=str)

wholefoods_data = pd.read_csv(
    'C:\\...')


try:
    search_input = driver.find_element_by_id('store-finder-search-bar')

    for index in range(len(zipcode_data)):  # for each zip code

        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        search_input.clear()
        search_input.send_keys(zipcode)
        search_input.send_keys(u'\ue007')
        time.sleep(1)
        stores = driver.find_elements_by_xpath(
            '//*[@id="w-store-finder__store-list"]/wfm-store-list/ul/li')

        for store in range(1, (len(stores) + 1)):
            try:
                # get ID of store
                ID = driver.find_element_by_xpath(
                    '//*[@id="w-store-finder__store-list"]/wfm-store-list/ul/li[' + str(store) + ']').get_attribute('data-bu')

                # name of store
                name = WebDriverWait(driver, 15).until(
                    ec.presence_of_element_located((By.XPATH,  '//*[@id="w-store-finder__store-list"]/wfm-store-list/ul/li[' +
                                                    str(store) + ']/wfm-store-details/div/div[1]/a')))
                name = name.text

                address = driver.find_element_by_xpath('//*[@id="w-store-finder__store-list"]/wfm-store-list/ul/li[' +
                                                       str(store) + ']/wfm-store-details/div/div[3]/div[1]').text
                loc = driver.find_element_by_xpath('//*[@id="w-store-finder__store-list"]/wfm-store-list/ul/li[' +
                                                   str(store) + ']/wfm-store-details/div/div[3]/div[2]').text
                city = loc.split(',')[0]
                state = loc.split(',')[1].split(' ')[1]
                zipcode_real = loc.split(',')[1].split(' ')[2]

                # if there is no phone, set it to None
                try:
                    phone = driver.find_element_by_xpath('//*[@id="w-store-finder__store-list"]/wfm-store-list/ul/li['+str(
                        store)+']/wfm-store-details/div/div[4]/wfm-phone-number/a/span').text
                except:
                    phone = None

                # if store is already in dataframe skip it, otherwise add it to dataframe
                if (ID in wholefoods_data['ID'].values):
                    continue
                else:
                    wholefoods_data = wholefoods_data.append({'ID': ID, 'Phone': phone, 'Name': name, 'Address': address, 'City': city,
                                                              'State': state, 'Zipcode (real)': zipcode_real,  'Zipcode_testing(dont use this)': zipcode}, ignore_index=True)
            except Exception as e:
                # print zipcode, store index and exception details
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(zipcode, store, e, exc_type, fname, exc_tb.tb_lineno)
                continue
except Exception as e:
    print(e)
finally:
    wholefoods_data.to_csv(r'C:\\...',
                           index=False, header=True)
