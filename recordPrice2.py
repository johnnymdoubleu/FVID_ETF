import pandas as pd
from tigeraddele import addPrice


url ='https://www.tigeretf.com/front/products/product.do?ksdFund=KR7102110004&fundTypeCode=01000100#productTab'
ae = addPrice()
data = ae.getPrice(url) #retrieving the key information

crawled = [0]*9
# data = ["2019.07.11","27,320","27,321.20"]
mp = float(data[1].replace(',', ''))
nav = float(data[2].replace(',', ''))

df = pd.read_csv("D:\\Documents\\FVID_ETF\\tigeretf\\tiger200price.csv",encoding='utf-8')

df = pd.DataFrame(df)

#calculating the difference and the percentage change of market price
change1 = str("{0:.0f}".format(mp - float(df.iloc[0,1].replace(',', ''))))
pcent1 = "{0:.2f}".format((float(change1) / float(df.iloc[0,1].replace(',', ''))) * 100)
if float(change1) < 0:
    pcent1 = "-" + pcent1  +"%"
else : pcent1 = pcent1 +"%"

#calculating the difference and the percentage change 기준 price
change2 = str("{0:.2f}".format(nav - float(df.iloc[0,5].replace(',', ''))))
pcent2 = "{0:.2f}".format((float(change2) / float(df.iloc[0,5].replace(',', ''))) * 100)
if float(change2) < 0:
    pcent2 = "-" + pcent2 +"%"
else : pcent2 = pcent2 +"%"

premdisc = str("{0:.2f}".format((mp-nav)/nav * 100))
premdisc = premdisc + "%"
# if float(premdisc) < 0:
#     premdisc = "-" + premdisc +"%"
# else : premdisc = premdisc +"%"

crawled[0] = data[0]  #쫌더 효율 적인 코드가 필요함
crawled[1] = data[1]
crawled[2] = change1
crawled[3] = pcent1
crawled[4] = ""
crawled[5] = data[2]
crawled[6] = change2
crawled[7] = pcent2
crawled[8] = premdisc

if int(crawled[0][-2:]) >int((df.iloc[0,0])[-2:]):
    # crawled[0] = int(crawled[0])
    df.loc[-1] = crawled  # adding a row
    df.index = df.index + 1  # shifting index
    df.sort_index(inplace=True)
    df.iloc[:,0] = df.iloc[:,0].astype(int,errors='ignore')
else :
    print("The same date already exists")


print(crawled)
print('\n converting to csv format ==============>')
print(df)

df.to_csv("D:\\Documents\\FVID_ETF\\tigeretf\\tiger200price.csv",index=False, encoding='utf_8_sig')
print('Download Completed')
