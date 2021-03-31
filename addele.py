from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import time
import re



class addPrice(object):
    def __init__(self):
        #chromedriver.exe가 이 파일과 같은 곳에 있기만 하면됩니다.
        self.driver = webdriver.Chrome(executable_path="./chromedriver")

    def getPrice(self,url):
        self.driver.get(url)

        time.sleep(2)

        button = self.driver.find_element_by_xpath('//li[a/@href="#subTab2"]')
        button.click()

        time.sleep(2)

        soup = bs(self.driver.page_source, "html.parser")
        div = soup.find_all('div',{'class':'table-area'})
        table = soup.find('table',{'class':'table detail-price-table'})

        rows = list()
        for td in table.find_all('td'):
            rows.append(td)

        match = re.search(r'\d{4}.\d{2}.\d{2}', rows[0].text)
        latestDate = match.group(0).replace('.', '')
        marketPrice = rows[1].text
        gijunPrice = rows[3].text

        crawled = [latestDate,marketPrice,gijunPrice]

        return crawled


# url ='http://www.kodex.com/product_view.do?fId=2ETF01'
# driver = webdriver.Chrome(executable_path="./chromedriver")
# driver.get(url)
#
# time.sleep(2)
#
# button = driver.find_element_by_xpath('//li[a/@href="#subTab2"]')
# button.click()
#
# time.sleep(2)
# soup = bs(driver.page_source, "html.parser")
# div = soup.find_all('div',{'class':'table-area'})
# table = soup.find('table',{'class':'table detail-price-table'})
#
# rows = list()
# for td in table.find_all('td'):
#     rows.append(td)
#
# match = re.search(r'\d{4}.\d{2}.\d{2}', rows[0].text)
# # latestDate = str(match.group(0))
# latestDate = match.group(0).replace('.', '')
# marketPrice = rows[1].text
# gijunPrice = rows[3].text
#
# crawled = [latestDate,marketPrice,gijunPrice]
# print(crawled)
