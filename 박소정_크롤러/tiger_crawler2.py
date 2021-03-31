from urllib import request
import os
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests

#상품코드 만들기
response = requests.get('https://www.tigeretf.com/front/products/index.do?pageType=2')
soup = BeautifulSoup(response.content, 'html.parser')

code_dict = {}

for li in soup.find_all('li'):
    a = li.find('a')
    name = a.text
    name = name.replace(' ', '_')
    href = str(a.get('href'))[35:47]
    if 'TIGER' in name:
        code_dict[name] = href


#크롤러

t1 = time.time()

class tiger_crawler2:
    def __init__(self, path_download, date, name):
        self.path_download = path_download
        self.date = str(date)[:11]
        self.name = name
        self.code = code_dict[str(name)]

    def get_download(self):
        url = 'https://www.tigeretf.com/front/products/excel/pdfExcel.do?ksdFund=' + str(self.code) + '&wkdate=' + str(self.date)
        filename = str(self.name) + '_' + str(self.date) +'.xls'
        os.chdir(self.path_download)
        request.urlretrieve(url, filename)

'''dt_index1 = pd.date_range(start='20190501', end='20190701', freq='B')
for i in dt_index1:
    a = tiger_crawler2('C:\\Users\\parks\\Desktop\\ETF2', i, name='TIGER_200')
    a.get_download()
time.sleep(10)

dt_index2 = pd.date_range(start='20190301', end='20190430', freq='B')
for i in dt_index2:
    a = tiger_crawler2('C:\\Users\\parks\\Desktop\\ETF2', i, name='TIGER_200')
    a.get_download()
time.sleep(10)

dt_index3 = pd.date_range(start='20190101', end='20190228', freq='B')
for i in dt_index3:
    a = tiger_crawler2('C:\\Users\\parks\\Desktop\\ETF2', i, name='TIGER_200')
    a.get_download()'''

index1 = pd.date_range(start='20190601', end='20190630', freq='B')
for i in index1:
    a = tiger_crawler2('C:\\Users\\parks\\Desktop\\ETF', i, name='TIGER_200')
    a.get_download()

for i in index1:
    b = tiger_crawler2('C:\\Users\\parks\\Desktop\\ETF', i, name='TIGER_KRX300')
    b.get_download()

for i in index1:
    c = tiger_crawler2('C:\\Users\\parks\\Desktop\\ETF', i, name='TIGER_코스피')
    c.get_download()

t2 = time.time()

print('다운로드가 완료되었습니다.')
print('걸린 시간:', t2-t1)

#1부터 10까지? 는 왜 이상하지