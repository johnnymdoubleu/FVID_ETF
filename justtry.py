import requests
import pandas as pd
from io import BytesIO

gen_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?name=fileDown&filetype=xls&url=MKD/13/1302/13020402/mkd13020402&market_gubun=ALL&lmt_tp=1&sect_tp_cd=ALL&schdate=20190708&pagePath=%2Fcontents%2FMKD%2F13%2F1302%2F13020402%2FMKD13020402.jsp'
query_str_parms = {
    'name': 'fileDown',
    'filetype': 'xls',
    'url': 'MKD/13/1302/13020402/mkd13020402',
    'market_gubun': 'ALL',
    'lmt_tp': '1',
    'sect_tp_cd': 'ALL',
    'schdate': '20180712',
    'pagePath': '/contents/MKD/13/1302/13020402/MKD13020402.jsp'
}

r = requests.get(gen_req_url, query_str_parms)

gen_req_url = 'http://file.krx.co.kr/download.jspx'
headers = {
    'Referer' : 'http://marketdata.krx.co.kr/mdi'
}
form_data = {
    'code': r.content
}
r = requests.post(gen_req_url, form_data)

df = pd.read_excel(BytesIO(r.content))
df['거래일자'] = 20180712

file_dir = 'D://Documents//FVID_ETF//krx'
file_name = 'KRX_81006_20180712.xlsx'

df.to_excel(file_dir + file_name,
            index=False, index_label=None)
