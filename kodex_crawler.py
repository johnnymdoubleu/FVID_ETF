from urllib import request
import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

#상품코드 만들기
response = requests.get('http://www.kodex.com/libpdf.do')
soup = BeautifulSoup(response.content, 'html.parser')

code_dict = {}

for a in soup.find_all('a'):
    k = [a.text, a.get('href')]
    if '/product_view' in k[1]:
        k[1] = k[1][25:]
        k[0] = k[0].replace(' ', '_')
        code_dict[k[0]] = k[1]

print(code_dict)


#크롤러 코드
t1 = time.time()
class KODEX_crawler:
    def __init__(self, path_download, date, name):
        self.path_download = path_download
        self.date = str(date)[:4] + str(date)[5:7] + str(date)[8:10]
        self.name = name
        self.code = code_dict[str(name)]

    def get_download(self):
        url = 'http://www.kodex.com/excel_pdf.do?fId=2ETF' + self.code + '&gijunYMD='+ str(self.date)
        filename = self.name + '_' + str(self.date)+'.xls'
        os.chdir(self.path_download)
        request.urlretrieve(url, filename)

'''dt_index1 = pd.date_range(start='20190501', end='20190701', freq='B')
for i in dt_index1:
    a = KODEX_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KODEX_200')
    a.get_download()
time.sleep(10)

dt_index2 = pd.date_range(start='20190301', end='20190430', freq='B')
for i in dt_index2:
    a = KODEX_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KODEX_200')
    a.get_download()
time.sleep(10)

dt_index3 = pd.date_range(start='20190101', end='20190228', freq='B')
for i in dt_index3:
    a = KODEX_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KODEX_200')
    a.get_download()'''

'''index1 = pd.date_range(start='20190601', end='20190630', freq='B')
for i in index1:
    a = KODEX_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KODEX_200')
    a.get_download()
    
for i in index1:
    b = KODEX_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KODEX_KTOP30')
    b.get_download()
for i in index1:
    c = KODEX_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KODEX_반도체')
    c.get_download()'''

t2 = time.time()

print('다운로드가 완료되었습니다.')
print('걸린 시간:', t2-t1)

# 20190501, 20190506 이상함.
# 중간중간 내용이 없는 파일들이 존재함. 주말이 아닌데도. 이런 데이터들은 어떻게 처리?? 데이터가 빌 때의 response 토대로 처리.
# 받은 파일 날짜와 파일명 매칭하는 데이터프레임 (크롤링 결과 정리하는)
# krx에 모든 etf 발행일.
# 기업들 이름이 바뀌는 문제
# 언제부터 크롤하는지의 문제
# 년도가 바뀔 때 path가 변함