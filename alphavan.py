from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ts = TimeSeries(key='ZZCEDAXI8ZIXHJX4',output_format='pandas')
# names = pd.read_csv("D:\\Documents\\FVID_Glassdoor\\2018_SnP500_Names.csv",encoding='utf-8')

# print(names)
tickk = []

# driver = webdriver.Chrome(executable_path="./chromedriver")
# names =['Cboe Global Markets, Inc.', 'Cintas Corporation', 'Connecticut General Corporation', 'National Association','Union Electric Company',  'Ohio Edison Company', 'Pacific Enterprises Inc.', 'Red Hat, Inc.', 'L3 Technologies, Inc.','Kansas Power & Light Co', 'Brown-Forman Corporation',  'NRG Energy, Inc.', 'The Charles Schwab Corporation']

# symbol =['NYSE:CAT', 'NASDAQ:SIVB', 'BATS:CBOE', 'NASDAQ:AAPL', 'NYSE:DGX', 'NYSE:APA', 'NASDAQ:FAST', 'NYSE:AAP', 'NASDAQ:MXIM', 'NASDAQ:SBAC', 'NYSE:CHD', 'NASDAQ:CTAS', 'NASDAQ:BIIB', '-', 'NYSE:D', 'NASDAQ:WDC', 'NYSE:PXD', 'NYSE:ES', 'NYSE:DLR', 'NASDAQ:ZION', 'NYSE:NBL', 'NYSE:CRM', 'NASDAQ:FLIR', 'NASDAQ:CPRT', 'OTCMKTS:UELMO', 'NYSE:FIS', 'NYSE:BHGE', 'NYSE:TAP', 'NYSE:IR', 'NYSE:PGR', 'NYSE:COP', '-', 'NYSE:ESS', 'NYSE:EL', '-', 'NYSE:PKI', 'NYSE:HIG', 'NASDAQ:KLAC', 'BMV:RHT', 'NASDAQ:CELG', 'NYSE:DAL', 'NASDAQ:DISCA', 'NASDAQ:TSCO', 'NYSE:PNW', 'NYSE:WFC', 'NYSE:C', '-', 'NYSE:PWR', '-', 'NYSE:BLL', 'NYSE:AIV', 'NASDAQ:VRSK', 'NASDAQ:ALGN', 'NYSE:HCP', 'NASDAQ:CTSH', '-', 'NYSE:BF.B', 'NYSE:AMT', 'NASDAQ:REGN', 'NASDAQ:ETFC', 'NYSE:GLW', 'NYSE:MGM', 'NYSE:F', 'NASDAQ:VIAB', 'NYSE:SJM', 'NASDAQ:PBCT', 'NYSE:BA', 'NASDAQ:IPGP', 'NYSE:USB', 'NYSE:NRG', 'NYSE:SCHW']
exception=[]

for i in range(len(names)):
    compName = names[i]
    ticker = symbol[i]
    try :
        ticker = ticker.replace(' ','')

        time.sleep(1)
        print('Crawling ' + ticker + ' stock prices \n')

        if '.' in ticker:
            tic = ticker.split(":")[1]
            df, meta_data = ts.get_daily(symbol=tic, outputsize='full')

        else:
            df, meta_data = ts.get_daily(symbol=ticker, outputsize='full')

        df.columns = ['open','high','low','close','volume']
        df.reset_index(level=0, inplace=True)
        compName = compName.replace(',', '')
        compName = compName.replace('.','')
        df.to_csv("D:\\Documents\\FVID_Glassdoor\\Stocks\\" + compName + ".csv",index=False, encoding='utf_8_sig')
        print(ticker + ' stock price retrieval completed \n\n')
        print('Number of crawled Stocks : ', i+1-len(exception))
    except Exception:
        print('Exception Exist for ' + compName + '\n\n')
        exception.append(compName)
        tickk.append(ticker)
        pass
        time.sleep(2)


# for i in range(len(names)):
#     compName = names.iloc[i,0]
#     ticker = names.iloc[i,1]
#     try :
#         ticker = ticker.replace(' ','')
#
#         time.sleep(1)
#         print('Crawling ' + ticker + ' stock prices \n')
#
#         if '.' in ticker:
#             tic = ticker.split(":")[1]
#             df, meta_data = ts.get_daily(symbol=tic, outputsize='full')
#
#         else:
#             df, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
#
#         df.columns = ['open','high','low','close','volume']
#         df.reset_index(level=0, inplace=True)
#         compName = compName.replace(',', '')
#         compName = compName.replace('.','')
#         df.to_csv("D:\\Documents\\FVID_Glassdoor\\Stocks\\" + compName + ".csv",index=False, encoding='utf_8_sig')
#         print(ticker + ' stock price retrieval completed \n\n')
#         print('Number of crawled Stocks : ', i+1-len(exception))
#     except Exception:
#         print('Exception Exist for ' + compName + '\n\n')
#         exception.append(compName)
#         tickk.append(ticker)
#         pass
#         time.sleep(2)




# for i in range(len(names)):
#     try :
#         compName = names.iloc[i,0]
#         compName = compName.replace('The ', '')
#         compName = compName.replace(' (US)','')
#         driver.get('https://www.google.com')
#         search=driver.find_element_by_name('q')
#         search.send_keys(compName + ' stock price')
#         search.send_keys(Keys.RETURN)
#         time.sleep(2)
#         if driver.find_element_by_xpath('//span[@class="HfMth"]').text :
#             ticker = driver.find_element_by_xpath('//span[@class="HfMth"]').text
#         else :
#             driver.get('https://www.google.com')
#             search=driver.find_element_by_name('q')
#             search.send_keys(compName + ' stock symbol')
#             search.send_keys(Keys.RETURN)
#             time.sleep(2)
#             ticker = driver.find_element_by_xpath('//span[@class="HfMth"]').text
#         symbol.append(ticker)
#         print(ticker)
#     except Exception:
#         ticker = '-'
#         symbol.append(ticker)
#         print(ticker)

print(exception)
print(tickk)
print(len(tickk))
