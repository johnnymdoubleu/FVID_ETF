from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
import datetime as dt
import os

email = 'flamewndls@gmail.com'
pw = 'xkq4q5yi'


class Scrapper(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver") #chromedriver.exe가 이 파일과 같은 곳에 있기만 하면됩니다.
        self.wait = WebDriverWait(self.driver, 5)
        self.page_source = ''
        self.login()

    def login(self):
        try:
            self.driver.get("https://www.morningstar.com/sign-in")
            emailAddress = self.wait.until(EC.presence_of_element_located((By.NAME, "userName")))
            passWord = self.driver.find_element_by_name("password")
            emailAddress.send_keys(email)
            passWord.send_keys(pw)
            passWord.send_keys(Keys.RETURN)

        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found on glassdoor.com")
            exit()

    def getCode(self):
        self.driver.get('https://finance.naver.com/sise/etf.nhn')
        # time.sleep(3)
        # nextTab = self.driver.find_element_by_xpath('//li[@class="tab2 _etf_tab"]')
        # nextTab.click()

        time.sleep(2)
        soup = bs(self.driver.page_source,"html.parser")

        table = soup.find('tbody', {'id':'etfItemTable'})
        abnormally = ['69660','91170','91160','99140', '91180','91230','98560', '97750', '91210', '91220']
        gicode = list()
        for i in table.find_all("a", href=re.compile("code")):
            code = i.attrs['href'][-6:]
            if code[0] == '0':
                code = code[1:]

            if code in abnormally:
                code = '0' + code
            gicode.append(code)

        return gicode

    def dismissButton(self):
        try :
            dismiss = self.driver.find_element_by_xpath('//button[@class="mdc-button mds-button mdc-overlay__button mds-button--secondary mdc-button--secondary-fill mds-button--large"]')
            dismiss.click()
        except Exception:
            pass

    def searchETF(self,code):
        self.driver.get('https://www.morningstar.com/etfs/xkrx/'+code+'/quote')
        time.sleep(3)
        try :
            dismiss = self.driver.find_element_by_xpath('//button[@class="mdc-button mds-button mdc-overlay__button mds-button--secondary mdc-button--secondary-fill mds-button--large"]')
            dismiss.click()
        except Exception:
            pass

        self.page_source = self.driver.page_source
        return self.page_source

    def getETFname(self):
        soup = bs(self.page_source, 'html.parser')
        etf = soup.find('span',{'itemprop': 'name'}).text
        return etf

    def getQuote(self,code):
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="sal-snap-panel"]')))

        quote=[]
        soup = bs(self.driver.page_source,"html.parser")
        etf = soup.find('span',{'itemprop': 'name'}).text
        etf = etf.replace(' ','_')
        etf = etf.replace('KIM_','')
        etf=etf.replace('rirang','RIRANG')
        lee=soup.find_all('li',{'class':'sal-snap-panel'})
        indexlist = []
        for i in range(12,23):
            name = lee[i].find('div',{'class':'sal-dp-name ng-binding'}).text
            name = str(name).replace('  ', '')
            name = str(name).replace('\n', '')
            indexlist.append(name)
            mw = lee[i].find('div',{'class':'sal-dp-value ng-binding'})
            if mw == None:
                mw = lee[i].find('div',{'class':'sal-dp-value ng-binding ng-scope'})
            value=mw.text
            value = str(value).replace(' - ', '')
            value = str(value).replace('  ', '')
            value = str(value).replace('\n', '')
            quote.append(value)

        div = soup.find('div',{'class':'sal-mip-quote__indicate ng-scope'})
        date = div.find_all('span')[3].text
        date=date.split('as of ')[1]
        date=date.replace(' PM KST','')
        date=date.replace(' AM KST','')
        date= dt.datetime.strptime(date, '%b %d, %Y, %H:%M').strftime('%Y%m%d')
        # date=date.replace(':','')
        df = pd.DataFrame(quote,columns=['Values'],index=indexlist)
        if not os.path.exists("D:\\Documents\\FVID_ETF\\CrawlETFdata\\"+ etf +'\\'):
            os.makedirs("D:\\Documents\\FVID_ETF\\CrawlETFdata\\"+ etf +'\\')
        time.sleep(1)
        df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\"+ etf +'\\'+code+'_' +date +"_Quote.csv", encoding='utf_8_sig')



        return df

    def getPerformance(self,code):
        performanceChart = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="/etfs/xkrx/' + code + '/performance"]')))
        # performanceChart = self.driver.find_element_by_xpath('//a[@href="/etfs/xkrx/' + code + '/performance"]')
        performanceChart.click()

        time.sleep(2)
        soup = bs(self.driver.page_source,"html.parser")
        etf = soup.find('span',{'itemprop': 'name'}).text
        etf = etf.replace(' ','_')
        etf = etf.replace('KIM_','')
        etf=etf.replace('rirang','RIRANG')
        div = soup.find('table',{'class','total-table'})

        smalllist = []
        listOfLists = [[] for i in range(6)]
        iter = 0

        for i in div.find_all('tr',{'class','ng-scope'}) :
            for j in i.find_all('span',{'class','ng-binding ng-scope'}):
                value = j.text
                smalllist.append(value)
            if len(smalllist) != 11 :
                smalllist = []
            else :
                listOfLists[iter] = smalllist
                smalllist = []
                iter += 1

            if iter == 6:
                break
        date = soup.find('span',{'class':'date ng-binding'}).text
        date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
        df = pd.DataFrame(listOfLists,columns=['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','YTD'],
                index=['Fund (Price)','Fund (NAV)','+/ Category (NAV)', '+/- Index (Price)','Percentile Rank','# of Funds in Category'])

        df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\" + etf+'\\'+code + '_'+ date +"_Growth10000.csv", encoding='utf_8_sig')
        return df

    def getTrailing(self,code):
        time.sleep(2)
        soup = bs(self.driver.page_source,"html.parser")
        etf = soup.find('span',{'itemprop': 'name'}).text
        etf = etf.replace(' ','_')
        etf = etf.replace('KIM_','')
        etf=etf.replace('rirang','RIRANG')
        div = soup.find('div',{'class','sal-trailing-return__left performance-table-pinned'})
        length = div.find_all('td',{'class':'ng-binding'})
        indexlist = []
        for i in length:
            johnny = i.text
            johnny = johnny.replace('\n','')
            indexlist.append(johnny)

        smalllist = []
        listOfLists = [[] for i in range(5)]
        iter = 0
        div = soup.find('div',{'class','sal-trailing-return__middle'})
        for i in div.find_all('tr') :
            for j in i.find_all('td'):
                value = j.text
                value=value.replace('\n','')
                value=value.replace('  ','')
                smalllist.append(value)
            if len(smalllist) != 11 :
                smalllist = []
            else :
                listOfLists[iter] = smalllist
                smalllist = []
                iter += 1

            if iter == 5:
                break
        date = soup.find('span',{'class':'date ng-binding'}).text
        date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
        df = pd.DataFrame(listOfLists[1:],columns=listOfLists[0],index=indexlist[0:4])
        df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\" + etf +'\\'+code+ '_'+ date +"_TrailingReturn.csv", encoding='utf_8_sig')
        try :
            dismiss = self.driver.find_element_by_xpath('//button[@class="mdc-button mds-button mdc-overlay__button mds-button--secondary mdc-button--secondary-fill mds-button--large"]')
            dismiss.click()
        except Exception:
            pass
        return df

    def getRisk(self,code):
        try :

            time.sleep(3)
            risk = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="/etfs/xkrx/' + code + '/risk"]')))
            # risk = self.driver.find_element_by_xpath('//a[@href="/etfs/xkrx/' + code + '/risk"]')
            risk.click()

            time.sleep(3)

            soup = bs(self.driver.page_source,'html.parser')
            etf = soup.find('span',{'itemprop': 'name'}).text
            etf = etf.replace(' ','_')
            etf = etf.replace('KIM_','')
            etf=etf.replace('rirang','RIRANG')
            div = soup.find('div',{'class':'sal-risk-volatility-measures__dataTable'})
            columnlist=[]
            for i in div.find_all('th'):
                columnlist.append(i.text)

            smalllist = []
            indexlist = []
            listOfLists = [[] for i in range(5)]
            iter = 0

            for i in div.find_all('tr',{'class','ng-scope'}) :
                for j in i.find_all('span',{'class','ng-binding'}):
                    value = j.text
                    smalllist.append(value)

                listOfLists[iter] = smalllist[1:]
                indexlist.append(smalllist[0])
                smalllist = []
                iter += 1

            div = soup.find('div',{'class':'sal-risk-volatility-measures__footer'})
            date = div.find_all('span',{'class':'ng-binding ng-scope'})[1].text
            date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
            df = pd.DataFrame(listOfLists,columns=columnlist[1:],index=indexlist)
            # df = df.set_index('Trailing')
            df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\" + etf+'\\'+code + '_'+ date +"_Risk.csv", encoding='utf_8_sig')
            return df
        except Exception:
            pass

    def getAssetAllo(self,code):
        try :
            time.sleep(2)
            portfolio = self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="/etfs/xkrx/' + code + '/portfolio"]')))
            portfolio.click()
            time.sleep(3)
            # self.wait.until(EC.presence_of_element_located((By.XPATH, '//th[@class="ng-binding ng-scope"]')))
            soup = bs(self.driver.page_source,'html.parser')
            etf = soup.find('span',{'itemprop': 'name'}).text
            etf = etf.replace(' ','_')
            etf = etf.replace('KIM_','')
            etf=etf.replace('rirang','RIRANG')
            div = soup.find('div',{'class':'sal-columns sal-small-12 sal-asset-allocation__assetTable sal-medium-8'})

            if div == None : ##종종 performance 탭에 오류가 생기는데 html이 다른것들과 변형이 되었기에 오류가 생김. (오류 케이스 수정)
                div = soup.find('div',{'class':'sal-columns sal-small-12 sal-asset-allocation__assetTable'})


            columnlist = []
            for i in div.find_all('th'):
                columnlist.append(i.text)

            indexlist = []
            smalllist = []
            listOfLists = [[] for i in range(6)]
            iter = 0

            for i in div.find_all('tr',{'class','ng-scope'}) :
                value = i.find('td',{'class':'ng-binding'}).text
                value = value.replace('\n','')
                value = value.replace('  ','')
                indexlist.append(value)


                for j in i.find_all('td',{'class','ng-binding ng-scope'}):
                    value = j.text
                    value = value.replace('\n', '')
                    value = value.replace('  ', '')
                    smalllist.append(value)

                listOfLists[iter] = smalllist
                smalllist = []
                iter += 1

            div = soup.find('div',{'class':'sal-asset-allocation__footer'})
            date = div.find_all('span',{'class':'ng-binding ng-scope'})[0].text
            date = date.replace('\n','')
            date = date.replace('  ','')
            date=date.split('as of')[1]
            date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
            df = pd.DataFrame(listOfLists,columns=columnlist[1:],index=indexlist)
            df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\" + etf +'\\'+code+ '_'+ date +"_AssetAllocation.csv", encoding='utf_8_sig')
            return df
        except Exception:
            pass

    def getStockStyle(self,code):
        try :
            time.sleep(2)
            soup = bs(self.driver.page_source,"html.parser")
            etf = soup.find('span',{'itemprop': 'name'}).text
            etf = etf.replace(' ','_')
            etf = etf.replace('KIM_','')
            etf=etf.replace('rirang','RIRANG')
            div = soup.find('div',{'class','sal-stock-style__valueTable'})

            length = div.find_all('th',{'class':'ng-binding'})
            columnlist = []
            for i in length:
                johnny = i.text
                johnny = johnny.replace('&amp;','&')
                columnlist.append(johnny)

            indexlist=[]
            smalllist = []
            listOfLists = [[] for i in range(10)]
            iter = 0

            tbody=div.find('tbody')
            for i in tbody.find_all('tr') :
                for j in i.find_all('td'):
                    value = j.text
                    smalllist.append(value)

                listOfLists[iter] = smalllist[1:]
                indexlist.append(smalllist[0])
                smalllist = []
                iter += 1

                if iter == 11:
                    break

            div = soup.find('div',{'class':'sal-stock-style__tableFooter'})
            date = div.find_all('span',{'class':'ng-binding ng-scope'})[1].text
            date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
            df = pd.DataFrame(listOfLists,columns=columnlist[1:],index=indexlist)
            df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\"+ etf +'\\'+code+ '_'+ date +"_StockStyle.csv", encoding='utf_8_sig')
            return df
        except Exception:
            pass

    def getSectors(self,code):
        try:
            soup = bs(self.driver.page_source,'html.parser')
            etf = soup.find('span',{'itemprop': 'name'}).text
            etf = etf.replace(' ','_')
            etf = etf.replace('KIM_','')
            etf=etf.replace('rirang','RIRANG')
            div = soup.find('div',{'class':'sal-sector-exposure__sector-table-wrapper'})

            smalllist = []
            listOfLists = [[] for i in range(11)]
            iter = 0

            for i in div.find_all('tr',{'class','ng-scope'}) :
                for j in i.find_all('span',{'class','ng-binding'}):
                    value = j.text
                    value = str(value).replace('\n', '')
                    value = str(value).replace('  ', '')
                    smalllist.append(value)

                listOfLists[iter] = smalllist
                smalllist = []
                iter += 1

            date = soup.find('span',{'ng-if':'!vm.isFundDateEmpty'}).text
            date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
            df = pd.DataFrame(listOfLists,columns=['Sectors', 'Fund %','Category %'])
            df = df.set_index('Sectors')
            df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\"+ etf+'\\'+code + '_'+ date +"_Sectors.csv", encoding='utf_8_sig')
            return df
        except Exception:
            pass

    def getSustain(self,code):
        try :
            portfolio = self.driver.find_element_by_xpath('//a[@href="/etfs/xkrx/' + code + '/portfolio"]')
            portfolio.send_keys(Keys.PAGE_DOWN)
            portfolio.send_keys(Keys.PAGE_DOWN)
            portfolio.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            soup = bs(self.driver.page_source,"html.parser")
            etf = soup.find('span',{'itemprop': 'name'}).text
            etf = etf.replace(' ','_')
            etf = etf.replace('KIM_','')
            etf=etf.replace('rirang','RIRANG')
            indexlist = ['Sustainability Rate']
            smalllist =[]

            sustainability = soup.find('div',{'class':'sal-sustainability__rating ng-binding'}).text
            sustainability = sustainability.replace('\n','')
            sustainability = sustainability.replace('  ','')
            smalllist.append(sustainability)
            # print(sustainability)
            percentRank = soup.find('div',{'class':'sal-sustainability__category-rank sal-sustainability__percent-info ng-binding ng-scope'}).text
            percentRank = percentRank.replace('\n','')
            percentRank = percentRank.replace('  ','')
            indexlist.append(percentRank.split(':')[0])
            percentRank = percentRank.split(':')[1]
            percentRank = percentRank.replace(' ','') + '%'
            smalllist.append(percentRank)
            # print(percentRank)

            for i in soup.find_all('div',{'class':'sal-sustainability__dp-value ng-binding'}):
                value = i.text
                value = value.replace('\n','')
                value = value.replace('  ','')
                smalllist.append(value)

            for i in soup.find_all('div',{'class':'sal-sustainability__dp-title ng-binding'}):
                value = i.text
                value = value.replace('\n','')
                value = value.replace('  ','')
                value = value.replace('?','')
                if value != 'Most Recent Portfolio':
                    indexlist.append(value)

            # div = soup.find('div',{'class':'sal-row'})
            date=soup.find('span',{'ng-if':'vm.showSustainabilityRating'}).text
            date=date.split('as of ')[1]
            date= date.replace('.\xa0','')
            date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
            df = pd.DataFrame(smalllist,columns=['Values'],index=indexlist)
            df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\" + etf +'\\'+code+ '_'+ date +"_Sustainability.csv", encoding='utf_8_sig')
            return df
        except Exception:
            return('No result found for Sustainability')
            pass

    def getHoldings(self,code):
        try :
            portfolio = self.driver.find_element_by_xpath('//a[@href="/etfs/xkrx/'+ code + '/portfolio"]')
            portfolio.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            soup = bs(self.driver.page_source,"html.parser")
            etf = soup.find('span',{'itemprop': 'name'}).text
            etf = etf.replace(' ','_')
            etf = etf.replace('KIM_','')
            etf=etf.replace('rirang','RIRANG')
            indexlist = ['Current Porfolio Date']
            #
            div = soup.find('ul',{'class':'sal-mip-holdings__block-grid small-block-grid-6 medium-block-grid-6 large-block-grid-6 small-block-grid-5 medium-block-grid-5 large-block-grid-5'})
            smalllist =[div.find('div',{'class':'sal-dp-value ng-binding ng-scope'}).text]

            for i in div.find_all('div',{'class':'sal-dp-value ng-binding'}):
                value=i.text
                smalllist.append(value)

            for i in div.find_all('div',{'class':'sal-dp-name ng-binding'}):
                value= i.text
                indexlist.append(value)

            indexlist.append('% Assets in Top 10 Holdings')
            indexlist.append('Reported Turnover %')
            div = soup.find('div',{'class':'sal-holdings__footnote'})

            date = div.find('span',{'class','ng-binding ng-scope'}).text
            date=date.split('as of ')[1]
            date = date.replace(' | ','')
            date= dt.datetime.strptime(date, '%b %d, %Y').strftime('%Y%m%d')
            df = pd.DataFrame(smalllist,columns=['Values'],index=indexlist)
            df.to_csv("D:\\Documents\\FVID_ETF\\CrawlETFdata\\" + etf+'\\'+code + '_'+ date +"_Holdings.csv", encoding='utf_8_sig')
            return df

        except Exception:
            return('No result found for Holdings')
            pass
