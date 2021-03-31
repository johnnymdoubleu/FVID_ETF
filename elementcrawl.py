from urllib import request
import os
# import time
# import calendar
# import datetime
# from datetime import date
# import tox
# from workalendar.asia import SouthKorea


class elementCrawler:
    def __init__(self, path_download):
        self.path_download = path_download

    def requestOn(self, date):
        # url = 'http://www.kbam.co.kr/etf/kor/product/product_pdf_excel.jsp?&input_ym=' + str(date) +'&fundCd=4435'
        url = 'http://www.kodex.com/excel_standar.do?fId=2ETF01&gijunYMD='+str(date)
        filename = 'kodex3monthsprice_downloaded' + str(date) +'.csv'
        os.chdir(self.path_download)
        request.urlretrieve(url, filename)


date = 20190709
print('==> Downloading kodex 200 ETF price, date: ', date)
a = elementCrawler('D:\\Documents\\FVID_ETF\\kodexetf')
a.requestOn(date)


print('==> Download completed')
