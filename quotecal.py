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

codeid = '2ETF01'
date ='2019-08-02'

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get('http://www.kodex.com/product_view.do?fId='+codeid)
time.sleep(2)

soup = bs(driver.page_source, 'html.parser')
table = soup.find('table',{'class':'table type01'})
tbody = table.find('tbody')
ter = tbody.find_all('td',{'class':'tal'})[4].text
ter = ter.split('(')[0]
ter = ter.replace('연 ','')
ter = ter.replace('  ','')
ter = ter.replace('\n','')


button = driver.find_element_by_xpath('//a[@href="#subTab2"]')
button.click()
button.send_keys(Keys.PAGE_DOWN)
button.send_keys(Keys.PAGE_DOWN)
button.send_keys(Keys.PAGE_DOWN)
button.send_keys(Keys.PAGE_DOWN)

soup = bs(driver.page_source,'html.parser')
div = soup.find('table',{'class':'table detail-price-table'})
# print(div)
columnlist = ['date']
thread = div.find('tr',{'class':'rowTr'})
for i in thread.find_all('th'):
    columnlist.append(i.text)

tbody = div.find('tbody')
listOfLists = [[] for i in range(len(tbody.find_all('tr')))]
smalllist = []
iter = 0

for i in tbody.find_all('tr'):
    for j in i.find_all('td'):
        value=j.text
        value=value.replace(',','')
        value=value.replace('  ','')
        value=value.replace('\n','')
        smalllist.append(value)

    listOfLists[iter]= smalllist
    smalllist=[]
    iter += 1

df = pd.DataFrame(listOfLists,columns=columnlist)
# print(df)
pp = soup.find_all('p',{'class':'rate-price'})[0].text
pp = pp.replace(',','')
pp = pp.replace(' 원','')
inav = float(df.iloc[0,3])*(float(pp)/ float(df.iloc[0,1]))
nav = df.iloc[0,3]
pt = soup.find_all('p',{'class':'rate-price'})[2].text
pt = pt.replace(',','')
pt = pt.replace(' 주','')
# print(pp)


button = driver.find_element_by_id('idSubTab3')
button.click()
time.sleep(2)
button = driver.find_element_by_id('gijunYMD')
button.send_keys(Keys.CONTROL,'a')
button.send_keys(Keys.BACKSPACE)
button.send_keys(date)
button.send_keys(Keys.RETURN)
button.send_keys(Keys.RETURN)
time.sleep(2)
button = driver.find_element_by_id('btnPdfMore')
button.click()


time.sleep(2)
soup = bs(driver.page_source,"html.parser")

# button = driver.find_element_by_class_name('btn-type01 btn-date-check')
# button.click()
div= soup.find('table',{'class':'table detail-pdf-table'})
table =div.find('tbody',{'id':'pdfResultList'})
# print(len(table.find_all('tr')))
listOfLists = [[] for i in range(len(table.find_all('tr')))]
smalllist = []
iter = 0
for i in table.find_all('tr'):
    # print(i)
    for j in i.find_all('td'):
        value = j.text
        value = value.replace('  ','')
        value = value.replace('\n','')
        smalllist.append(value)

    listOfLists[iter]=smalllist
    smalllist = []
    iter += 1

columnlist = []
table = div.find('tr')
for i in table.find_all('th'):
    columnlist.append(i.text)

# print(columnlist)
df = pd.DataFrame(listOfLists,columns=columnlist)
df = df.iloc[:,1:]
# print(df)


netasset = 0
sum = 0
totalsum=0
for i in range(len(df.index)):
    # print(df.iloc[i,1])
    # print(i)
    if(len(df.iloc[i,1])==6):
        num = df.iloc[i,2].replace(',','')
        price = df.iloc[i,5].replace(',','')
        pp = df.iloc[i,4].replace(',','')
        sum = sum + float(pp)
        totalsum = totalsum + float(pp)
    else :
        tt = df.iloc[i,4].replace(',','')
        totalsum = totalsum + float(tt)

koreanS = (sum / totalsum) * 100
others = (float(tt) / totalsum) * 100


print('Quote : \n\n')
print('iNAV : ', inav)
print('NAV : ', nav)
print('Volume : ', pt)
print('Expense Ration : ', ter)
print('Bid/Ask/Spread : 25825 / 25725 / 0.02%')
driver.get('http://comp.fnguide.com/SVO2/ASP/etf_snapshot.asp?pGB=1&gicode=A069500&cID=&MenuYn=Y&ReportGB=&NewMenuID=401&stkGb=770')
time.sleep(2)
soup=bs(driver.page_source,'html.parser')

table = soup.find('table',{'class':'us_table_ty1 table-hb thbg_g h_fix zigbg_no'})
marprice = table.find_all('td')[0].text
marprice = marprice.split('/')[0]
marprice = marprice.replace(',','')
# print(marprice)
numstock = table.find_all('td')[5].text
numstock = numstock.replace(',','')
totalasset = float(marprice) * float(numstock)
print('Total Asset : ',totalasset)

yearhigh = table.find_all('td')[1].text
yearhigh = yearhigh.replace(',','')
yearlow = table.find_all('td')[2].text
yearlow = yearlow.replace(',','')
print('12 month yield : ', 2.27)
print('Day Range : 26210 - 26420')
print('Year Range : ' + yearlow + ' - ' + yearhigh)
print('Category : Korea Fund,  Korea Large-Cap Equity\n\n')


print('Top 10 holdings : \n\n',df.iloc[1:11,[0,1,3,5]].to_string(),'\n\n')
print('Asset Allocation : \n\n', pd.DataFrame({'Asset Class':['Korean Stock','Cash'],'Net Percentage' : [koreanS, others]}))
