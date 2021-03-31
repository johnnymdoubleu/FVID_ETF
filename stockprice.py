import pandas_datareader as pdr
import pandas as pd


exceptions= []

'''
S&P 500 주가 크롤러
'''

names = pd.read_csv("D:\\Documents\\FVID_Glassdoor\\2018_SnP500_Names.csv",encoding='utf-8')


for i in range(len(names)):
    try:
        compName = names.iloc[i,0]
        # compName = names[i]
        ticker = names.iloc[i,1]
        # ticker = tickk[i]
        ticker = ticker.split(':')[1]
        ticker= ticker.replace(' ','')
        ticker= ticker.replace('.','-')

        df=pdr.get_data_yahoo(ticker,'2009-01-01','2019-08-05')
        df.to_csv("D:\\Documents\\FVID_Glassdoor\\StockPrices\\" + compName + ".csv", encoding='utf_8_sig')
    except Exception:
        print(compName,' : ', ticker)
        exceptions.append({compName:ticker})
        pass

'''
KOSPI 200 주가 크롤러
'''

names = pd.read_csv("D:\\Documents\\FVID_Glassdoor\\2018_KOSPI200_Names.csv",encoding='utf-8')
# names = ['우리금융지주']
# tickk = ['316140']
for i in range(len(names)):
    try:
        compName = names.iloc[i,0]
        # compName = names[i]
        ticker = names.iloc[i,1]
        ticker = tickk[i]
        ticker = ticker.replace('a','')
        ticker = ticker + '.KS'


        df=pdr.get_data_yahoo(ticker,'2009-01-01','2019-08-05')
        df.to_csv("D:\\Documents\\FVID_Glassdoor\\KOSPIStockPrices\\" + compName + ".csv", encoding='utf_8_sig')
    except Exception:
        print(compName,' : ', ticker)
        exceptions.append({compName:ticker})
        pass

print(exceptions)
