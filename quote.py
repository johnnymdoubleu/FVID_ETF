import pandas as pd
import glob
import os
import datetime as dt-

files = glob.glob('D:\\Documents\\FVID_ETF\\CrawlETFdata\\*')
# fp = glob.glob('D:\\Documents\\FVID_ETF\\CrawlETFdata\\HANARO_200_ETF')

dfs = []
for fp in files:
    parentdir = fp.split('\\')[4]
    q=tr=g1=r=aa=se=st=su=h='NA'
    code = glob.glob(fp + '\\*.csv')[0].split('\\')[5]
    code = code.split('_')[0]
    if len(code) != 6:
        code = '0' + code
        code = str(code)

    for i in glob.glob(fp + '\\*.csv'):
        if '_Quote' in i:
            date = []
            bb = glob.glob(fp+'\\*_Quote.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            q = max(date)

        if '_TrailingReturn' in i:
            date = []
            bb = glob.glob(fp+'\\*_TrailingReturn.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            tr = max(date)


        if '_Growth10000' in i:
            date = []
            bb = glob.glob(fp+'\\*_Growth10000.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            g1 = max(date)


        if '_Risk' in i:
            date = []
            bb = glob.glob(fp+'\\*_Risk.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            r = max(date)


        if '_AssetAllocation' in i:
            date = []
            bb = glob.glob(fp+'\\*_AssetAllocation.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            aa = max(date)


        if '_Sectors' in i:
            date = []
            bb = glob.glob(fp+'\\*_Sectors.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            se = max(date)


        if '_StockStyle' in i:
            date = []
            bb = glob.glob(fp+'\\*_StockStyle.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            st = max(date)


        if '_Sustainability' in i:
            date = []
            bb = glob.glob(fp+'\\*_Sustainability.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            su = max(date)


        if '_Holdings' in i:
            date = []
            bb = glob.glob(fp+'\\*_Holdings.csv')
            for j in bb:
                da = j.split('\\')[5]
                da = da.split('_')[1]
                da = dt.datetime.strptime(da,'%Y%m%d').strftime('%Y%m%d')
                date.append(da)
            h = max(date)



    check = {
        'ETF Name' : parentdir,
        'Code' : str(code),
        'Quote' : q,
        'Trailing Return' : tr,
        'Growth 10000' : g1,
        'Risk' : r,
        'Asset Allocations' : aa,
        'Sectors' : se,
        'StockStyle' : st,
        'Sustainability' : su,
        'Holdings' : h
    }
    dfs.append(check)

df = pd.DataFrame(dfs,columns=['ETF Name','Code','Quote','Trailing Return','Growth 10000','Risk','Asset Allocations','Sectors','StockStyle','Sustainability','Holdings'])
print(df)
df.to_csv("D:\\Documents\\FVID_ETF\\MorningstarDatabase.csv",index=False, encoding='utf_8_sig')
