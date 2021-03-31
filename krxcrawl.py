from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import time
import re
import os
import pandas as pd


options = webdriver.ChromeOptions()

preferences = {
    'download.default_directory':'D:\\Documents\\FVID_ETF\\krx'
    }
options.add_experimental_option('prefs',preferences)

driver = webdriver.Chrome(executable_path="./chromedriver",chrome_options=options)
print('Opening url ========================>')
driver.get('http://marketdata.krx.co.kr/mdi#document=080113')

time.sleep(2)

button = driver.find_element_by_xpath('//button[contains(text(), "CSV")]')
button.click()

time.sleep(3)

os.chdir('D:\\Documents\\FVID_ETF\\krx')
os.rename(src = 'data.csv',dst='listofetf.csv')
print('retrieving list of ETFs to csv format ========================>')


time.sleep(4)
df = pd.read_csv("D:\\Documents\\FVID_ETF\\krx\\listofetf.csv",encoding='utf-8')

df = pd.DataFrame(df)
etfdates = df.iloc[:,[2,6]]
print('extracting ETF list and published date')
print(etfdates)
