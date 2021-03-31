from urllib import request
import os
import pandas as pd
import time
import chardet

class kodexCrawler:
    def __init__(self, path_download):
        self.path_download = path_download

    def get_download(self, date):
        url = 'http://www.kodex.com/excel_pdf.do?fId=2ETF01&gijunYMD='+str(date)
        filename = 'kodex_200_'+str(date)+'.xls'
        os.chdir(self.path_download)
        request.urlretrieve(url, filename)

date = []
for i in range(1, 3):
    if len(str(i)) == 1:
        i = '0' + str(i)
    else :
        i = str(i)
    k = '201908'+i
    date.append(k)

for i in date:
    a = kodexCrawler('D:\\Documents\\FVID_ETF\\kodexetf')
    a.get_download(i)

print('Download completed')
time.sleep(2)

# with open('D:\\Documents\\FVID_ETF\\kodexetf\\kodex_200_20190802.csv', 'rb') as f:
#     result = chardet.detect(f.read())

df = pd.read_excel("D:\\Documents\\FVID_ETF\\kodexetf\\kodex_200_20190802.xls",skiprows=2,encoding='utf_8_sig')
df = df.iloc[:,1:]
print(df)
