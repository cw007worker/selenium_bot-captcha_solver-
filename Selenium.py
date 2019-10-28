from selenium import webdriver
#from bs4 import BeautifulSoup
import time
import os

import ctypes

test_c_codes = ctypes.cdll.LoadLibrary("RecogDll.dll")
DllInitialize = test_c_codes.DllInitialize
DllInitialize.restype = ctypes.c_bool

DllRecognizeTextFromFile = test_c_codes.DllRecognizeTextFromFile
DllRecognizeTextFromFile.restype = ctypes.c_char_p


DllDeInitialize = test_c_codes.DllDeInitialize


currentdir = "C:/Users/davidsmith/Desktop/Scrapping"


browser = webdriver.Chrome(
    'C:/Users/davidsmith/Desktop/Scrapping/chromedriver')


DllInitialize(100, 20, ctypes.c_char_p(currentdir.encode('utf-8')))

i = 1
while i <= 200:
    #browser = webdriver.Firefox('C:/webdriver/geckodriver')

    #driver = webdriver.Chrome('/Users/beomi/Downloads/chromedriver')

    browser.get(
        "https://servicesenligne2.ville.montreal.qc.ca/sel/evalweb/index")
    #html = browser.page_source
    #bs = BeautifulSoup(html,'html.parser')
    #imageurl = bs.find_all('', class_='form')

    divelement = browser.find_element_by_css_selector(
        "#type_recherche > div.ui-widget > div > img")
# C:\Users\davidsmith\Desktop\Scrapping\images
    s = "%03d" % (i)
    full_file_name = 'C:\\Users\\davidsmith\\Desktop\\Scrapping\\images\\' + s + '.png'
    fh = open(full_file_name, "wb")
    fh.write(divelement.screenshot_as_png)
    fh.close()
    i += 1

    #c_s = ctypes.c_char_p(full_file_name)

    recogtext = DllRecognizeTextFromFile(
        ctypes.c_char_p(full_file_name.encode('utf-8')))

    time.sleep(1)

    inputfield = browser.find_element_by_css_selector(
        "#type_recherche > div.ui-widget > div > input[type=text]")

    inputfield.send_keys(recogtext.decode('utf-8'))

    browser.find_element_by_css_selector("#type_recherche > button").click()

    time.sleep(5)

DllDeInitialize()
