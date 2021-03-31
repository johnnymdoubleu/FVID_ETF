from selenium import webdriver
import os
import time

chromedriver = 'D:\\Documents\\FVID_ETF\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

class tiger_crawler:
    def __init__(self, path_download):
        self.path_download = path_download

    def get_download(self, date):
        driver_down(date)
        time.sleep(0.5)
        if os.path.isfile(r"C:\Users\Parks\Downloads\PDF_DATA.xls"):
            os.rename(f"C:\\Users\\Parks\\Downloads\\PDF_DATA.xls", self.path_download)


def driver_move():
    driver.get(
        'https://www.tigeretf.com/front/products/product.do?ksdFund=KR7102110004&fundTypeCode=01000100#productTab')
    driver.execute_script('window.scrollTo(0, 200);')
    driver.find_element_by_xpath('''//*[@id="pdf"]/a''').click()
    driver.execute_script('window.scrollTo(0, 200);')

def driver_down(date):
    driver.find_element_by_xpath('''//*[@id="wkdate"]''').click()
    driver.find_element_by_xpath(f'''//*[@id="ui-datepicker-div"]/table/tbody/tr[{date[0]}]/td[{date[1]}]/a''').click()
    searchpdf = driver.find_element_by_class_name('searchPdf')
    driver.execute_script("arguments[0].click();", searchpdf)
    driver.execute_script('window.scrollTo(0, 200);')
    driver.find_element_by_xpath('''//*[@id="ajaxTab"]/div/dl/dd/a[2]/img''').click()


# 날짜 지정
datelist = []
num = 0
for i in range(4, 5):
    for j in range(2, 7):
        datelist.append((i, j, num+17))
        num += 1


driver_move()

for date in datelist:
    path_download = r"C:\Users\Parks\Desktop\ETF\tiger_200_2019-06-" + str(date[2]) + '.xls'
    cr = tiger_crawler(path_download)
    cr.get_download(date)
