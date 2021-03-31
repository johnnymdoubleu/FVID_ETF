
# http://www.kbam.co.kr/etf/kor/info/pdf.jsp#
# KB200을 크롤링함.
# 5월 1일 등 중간중간 이상정보가 섞여 있음. (엑셀파일로는 받아지는데, 안에 아무런 내용이 없음)

from urllib import request
import os
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests


#상품코드
response = requests.get('http://www.kbam.co.kr/etf/kor/info/pdf.jsp#')
soup = BeautifulSoup(response.content, 'html.parser')

dict_key = []
for tr in soup.find_all('tr'):
    if 'KBSTAR' in tr.text:
        k = (tr.text.strip()).split(' ')
        k = k[1:-1]
        codestr = ('_'.join(k))
        dict_key.append(codestr)

dict_value = []
for a in soup.find_all('a'):
    ao = str(a.get('onclick'))
    if 'saveExcel' in ao:
        v = ao.split(',')
        v = v[1][1:5]
        dict_value.append(v)

code_dict = {}
for i in range(len(dict_key)):
    code_dict[dict_key[i]] = dict_value[i]


#크롤러

t1 = time.time()

class KB_crawler:
    def __init__(self, path_download, date, name):
        self.path_download = path_download
        self.date = str(date)[:11].strip()
        self.name = name
        self.code = code_dict[str(name)]

    def get_download(self):
        url = 'http://www.kbam.co.kr/etf/kor/product/product_pdf_excel.jsp?&input_ym=' + str(self.date) + '&fundCd=' + str(self.code)
        filename = str(self.name) + '_' + str(self.date) + '.xls'
        os.chdir(self.path_download)
        request.urlretrieve(url, filename)


'''dt_index1 = pd.date_range(start='20190601', end='20190630', freq='B')
for i in dt_index1:
    a = KB_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KBSTAR_국고채3년')
    a.get_download()
    b = KB_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KBSTAR_200')
    b.get_download()
    c = KB_crawler('C:\\Users\\parks\\Desktop\\ETF', i, name='KBSTAR_헬스케어')
    c.get_download()'''

t2 = time.time()

print('다운로드가 완료되었습니다.')
print('걸린 시간:', t2-t1)
