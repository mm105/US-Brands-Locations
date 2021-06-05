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
    executable_path="C:\\...", options=options)
driver.get('https://www.cvs.com/store-locator/store-locator-landing.jsp;')
driver.maximize_window()

zipcode_data = pd.read_csv(
    'C:\\...',  dtype=str)

cvs_data = pd.read_csv(
    'C:\\...')

try:
    for index in range(len(zipcode_data)):  # for each zip code
        time.sleep(1)

        # get search bar element, if it is unavailable refresh page and try again
        try:
            search_input = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.ID, 'search')))
        except:
            driver.refresh()
            time.sleep(5)
            search_input = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.ID, 'search')))

        zipcode = zipcode_data.iloc[index]['ZIP_CODE']
        search_input.clear()
        # close popup ad if it appears
        try:
            driver.find_element_by_xpath(
                '//*[@id="acsMainInvite"]/div/a[1]').click()
        except:
            pass
        search_input.send_keys(zipcode)
        search_input.send_keys(u'\ue007')
        time.sleep(2)
        # get all <li> elements (i.e. stores), used to later get total number of stores for current zip code
        stores = driver.find_elements_by_xpath(
            '//*[@id="centerCol"]/ol/li')

        # close popup ad if it appears
        try:
            driver.find_element_by_xpath(
                '//*[@id="acsMainInvite"]/div/a[1]').click()
        except:
            pass

        for store in range(1, (len(stores))):  # for each store of current zip code
            try:
                # get ID of store
                ID = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR,  '#centerCol > ol > li:nth-child(' + str(
                        store+1) + ') > div > div.floatContainer.row.row1 > div.floatLeft.col.col1.fullWidth > div.srSection.floatLeft.numbers-wrap > div.store-number')))
                ID = ID.text

                # get full address and split it on address, city, state and zipcode of store
                loc = driver.find_element_by_css_selector('#centerCol > ol > li:nth-child('+str(
                    store+1)+') > div > div.floatContainer.row.row1 > div.floatLeft.col.col1.fullWidth > div.srAddress > div > a').text

                address = loc.split('\n')[0]
                city = loc.split('\n')[1].split(',')[0]
                state = loc.split('\n')[1].split(',')[1].split(' ')[1]
                zipcode_real = loc.split('\n')[1].split(',')[1].split(' ')[2]

                # if store is already in dataframe skip it, otherwise add it to dataframe
                if (ID in cvs_data['ID'].values):
                    continue
                else:
                    cvs_data = cvs_data.append(
                        {'ID': ID, 'Address': address, 'City': city, 'State': state, 'Zipcode (real)': zipcode_real,  'Zipcode_testing(dont use this)': zipcode}, ignore_index=True)
            except Exception as e:
                # exception for store number 1 occured because it is special <div> on page for "nearest open store" that sometimes is present and sometimes not.
                # This store will also be listed within <li> elements so we can skip it
                if store != 1:
                    # print zipcode, store index and exception details
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(
                        exc_tb.tb_frame.f_code.co_filename)[1]
                    print(zipcode, store, e, exc_type,
                          fname, exc_tb.tb_lineno)
                # continue with next zip code
                continue
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e, exc_type, fname, exc_tb.tb_lineno)
finally:
    cvs_data.to_csv(r'C:\\...',
                    index=False, header=True)
