from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
# from requests import get
import re

driver = webdriver.Chrome(executable_path="./chromedriver")

driver.get('https://finance.naver.com/sise/etf.nhn')
time.sleep(3)
nextTab = driver.find_element_by_xpath('//li[@class="tab2 _etf_tab"]')
nextTab.click()

time.sleep(2)
soup = bs(driver.page_source,"html.parser")

table = soup.find('tbody', {'id':'etfItemTable'})


gicode = list()
for i in table.find_all("a", href=re.compile("code")):
    gicode.append(i.attrs['href'][-6:])

print(gicode)

driver.get('http://comp.fnguide.com/SVO2/asp/SVD_Main.asp')

time.sleep(3)
increment = 0
try :
    for i in gicode:
        search= driver.find_element_by_id("SearchText")
        search.send_keys(i)
        search.send_keys(Keys.DOWN)
        search.send_keys(Keys.RETURN)

        soup = bs(driver.page_source, "html.parser")
        div = soup.find('div',{'class':'corp_group1'})
        etf = div.find('h1').text.strip()
        etf = str(etf).replace('\xa0', ' ')
        benchmark=soup.find('dd',{'class':'fl bench'}).text.strip()
        benchmark = str(benchmark).replace('\xa0', '')
        priceTable = soup.find('div',{'id':'etf1Price'})
        infoTable = soup.find('div',{'id':'etf1FundInfo'})


        elem = list()
        for ele in priceTable.find_all('td'):
            elem.append(ele.text)


        try :
            elements  = pd.DataFrame({
                'etfNAME' : etf,
                'code' : i,
                'benchmark' : benchmark,
                'f2max' : elem[1],
                'f2min' : elem[2],
                'TotalVol' : elem[5],
                'foregin' : elem[6] + "%",
                'TradeVol' : elem[7],
                'TradeVal' : elem[8]}, index=[0])
        except Exception:
            print("failed to retrieve information for ETF with code : " + i +'\n\n')
            pass
        print(elements)
        print('\n\n')
        increment +=1
except Exception:
    pass

print('total number of ETFs infromation retrieved : ' + str(increment))
