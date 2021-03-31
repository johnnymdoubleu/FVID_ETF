from urllib import request
import os

class tiger_crawler2:
    def __init__(self, path_download):
        self.path_download = path_download

    def get_download(self, date):
        url = 'https://www.tigeretf.com/front/products/excel/pdfExcel.do?ksdFund=KR7102110004&wkdate='+str(date)
        filename = 'tiger_200_'+str(date)+'.xls'
        os.chdir(self.path_download)
        request.urlretrieve(url, filename)

date = []
for i in range(20, 28):
    k = '2019-06-'+str(i)
    date.append(k)

for i in date:
    a = tiger_crawler2('D:\\Documents\\FVID_ETF\\tigeretf')
    a.get_download(i)

print('Download completed')

#1부터 10까지? 는 왜 이상하지
