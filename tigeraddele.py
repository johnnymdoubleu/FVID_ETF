from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time
import re



class addPrice(object):
    def __init__(self):
        #chromedriver.exe가 이 파일과 같은 곳에 있기만 하면됩니다.
        self.driver = webdriver.Chrome(executable_path="./chromedriver")

    def getPrice(self,url):
        self.driver.get(url)

        time.sleep(3)
        self.driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
        # self.driver.execute_script("scrollBy(0,250);")
        time.sleep(2)
        button = self.driver.find_element_by_xpath('//li[@id="price"]')
        # button.send_keys(Keys.HOME)
        # self.driver.execute_script("return arguments[0].scrollIntoView(true);", button)
        button.click()

        time.sleep(3)

        soup = bs(self.driver.page_source, "html.parser")
        div = soup.find_all('div',{'id':'profitDetail'})
        table = soup.find('tbody',{'id':'priceDetail'})

        rows = list()
        for td in table.find_all('td'):
            rows.append(td)

        latestDate = rows[0].text
        # match = re.search(r'\d{4}.\d{2}.\d{2}', rows[0].text)
        # latestDate = str(match.group(0))
        marketPrice = rows[1].text
        gijunPrice = rows[3].text

        crawled = [latestDate,marketPrice,gijunPrice]

        return crawled

    # def getVolume(self,url):
    #     self.driver.get(url)


# url ='https://www.tigeretf.com/front/products/product.do?ksdFund=KR7102110004&fundTypeCode=01000100#productTab'
# driver = webdriver.Chrome(executable_path="./chromedriver")
# driver.get(url)
#
# time.sleep(2)
#
# button = driver.find_element_by_xpath('//li[@id="price"]')
# button.click()
#
# time.sleep(2)
# soup = bs(driver.page_source, "html.parser")
# div = soup.find_all('div',{'id':'profitDetail'})
# table = soup.find('tbody',{'id':'priceDetail'})
#
# rows = list()
# for td in table.find_all('td'):
#     rows.append(td)
#
# match = re.search(r'\d{4}.\d{2}.\d{2}', rows[0].text)
# latestDate = str(match.group(0))
# marketPrice = rows[1].text
# gijunPrice = rows[3].text
#
# crawled = [latestDate,marketPrice,gijunPrice]
# print(crawled)
