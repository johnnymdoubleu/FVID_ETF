import pandas as pd
from selenium import webdriver
import time
import re

chromedriver = '/Users/jisujung/Desktop/서울대/개인 공부/인턴_glassdoor/chromedriver'
# 각자의 chromedriver 위치를 입력하시면 됩니다.


#연간, 분기별 투자 지표(수익성, 성장성, 안정성, 활동성)을 각각 dataframe으로 만들어 반환하는 함수입니다.
def get_tables(token):
    url= 'http://companyinfo.stock.naver.com/v1/company/c1040001.aspx?cmp_cd={}&cn='.format(token)
    driver= webdriver.Chrome(chromedriver)
    driver.get(url)
    time.sleep(1)

    profit= driver.find_element_by_xpath('//*[@id="val_tab1"]')
    growth= driver.find_element_by_xpath('//*[@id="val_tab2"]')
    stable= driver.find_element_by_xpath('//*[@id="val_tab3"]')
    active= driver.find_element_by_xpath('//*[@id="val_tab4"]')
    quarter= driver.find_element_by_xpath('//*[@id="frqTyp1"]')

    profit_y= pd.read_html(driver.page_source)
    time.sleep(1)

    growth.click()
    time.sleep(1)
    growth_y= pd.read_html(driver.page_source)
    time.sleep(1)

    stable.click()
    time.sleep(1)
    stable_y= pd.read_html(driver.page_source)
    time.sleep(1)

    active.click()
    time.sleep(1)
    active_y= pd.read_html(driver.page_source)
    time.sleep(1)

    quarter.click()
    time.sleep(0.5)
    profit.click()
    time.sleep(0.5)
    profit_q= pd.read_html(driver.page_source)
    time.sleep(1)

    growth.click()
    time.sleep(1)
    growth_q= pd.read_html(driver.page_source)
    time.sleep(1)

    stable.click()
    time.sleep(1)
    stable_q= pd.read_html(driver.page_source)
    time.sleep(1)

    active.click()
    time.sleep(1)
    active_q= pd.read_html(driver.page_source)

    return profit_y, profit_q, growth_y, growth_q, stable_y, stable_q, active_y, active_q


# 재무재표 데이터를 크롤하는 함수입니다.
def get_finance(token):
    url= 'http://companyinfo.stock.naver.com/v1/company/c1030001.aspx?cmp_cd={}&cn='.format(token)
    driver= webdriver.Chrome(chromedriver)
    driver.get(url)
    time.sleep(1)
    yearly= pd.read_html(driver.page_source)

    quarter= driver.find_element_by_xpath('//*[@id="frqTyp1"]')
    button= driver.find_element_by_xpath('//*[@id="hfinGubun"]')
    quarter.click()
    button.click()
    time.sleep(1)

    quarterly= pd.read_html(driver.page_source)

    return yearly, quarterly


# 투자지표와 재무재표 데이터를 받아 concat해 계산 식, 기본 정보, 연도/분기 별 투자지표, 연도/분기별 재무재표 총 4개의 dataframe을 반환하는 총괄함수입니다.
def to_db(token):
    py, pq, gy, gq, sy, sq, ay, aq= get_tables(token)
    time.sleep(1)
    year, quarter= get_finance(token)

    formula= py[3]
    formula = formula.drop(['분류'], axis=1)
    formula.set_index(formula['항목명'], inplace=True)
    formula.drop(['항목명'], axis=1, inplace=True)


    yearly_concat = pd.concat([py[6], gy[6], sy[6], ay[6]], ignore_index=True)
    temp = yearly_concat['항목']
    new = []
    for i in range(yearly_concat.shape[0]):
        word = temp[i]
        new.append(word.split(' ')[2])

    yearly_concat.drop(['항목'], axis=1, inplace=True)
    yearly_concat['항목'] = new
    yearly_concat.set_index(['항목'], inplace=True)


    quarterly_concat = pd.concat([pq[6], gq[6], sq[6], aq[6]], ignore_index=True)
    temp = quarterly_concat['항목']
    new = []
    for i in range(quarterly_concat.shape[0]):
        word = temp[i]
        new.append(word.split(' ')[2])

    quarterly_concat.drop(['항목'], axis=1, inplace=True)
    quarterly_concat['항목'] = new
    quarterly_concat.set_index(['항목'], inplace=True)

    stocks= py[9]
    temp = stocks['항목']
    new = []
    for i in range(stocks.shape[0] - 2):
        word = temp[i]
        new.append(word.split(' ')[2])

    new.append(temp[10])
    new.append(temp[11])

    stocks.drop(['항목'], axis=1, inplace=True)
    stocks['항목'] = new
    stocks.set_index(['항목'], inplace=True)


    investment= yearly_concat.merge(quarterly_concat, left_index=True,  right_index=True)


    financial = year[5].merge(quarter[5], left_on='항목', right_on='항목')
    temp = financial['항목']
    new = []
    for i in range(financial.shape[0]):
        word = temp[i]
        if '펼치기' in word:
            word = word.replace('펼치기', '')
            word = word.strip()
        new.append(word)

    financial.drop(['항목'], axis=1, inplace=True)
    financial['항목'] = new
    financial.set_index(['항목'], inplace=True)


    return formula,stocks, investment, financial


# 원하는 회사 이름을 입력하면 토큰을 반환하는 함수입니다.
def get_token(name, df):
    code= df[df['종목명']== name]['종목코드']
    token= str(code)
    finder= re.compile('[^a]*a(?P<token>[0-9]*)')
    m= re.search(finder, token)
    return m.group(1)


names = pd.read_csv('/Users/jisujung/Desktop/서울대/개인 공부/인턴_ETF/2018_KOSPI200_Names.csv')


# 원화는 회사 이름을 입력하면, 결과값이 저장됩니다.
if __name__ == '__main__':
    name= input('회사이름을 입력하세요: ')
    token= get_token(name, names)
    formula, stocks, investment, financial= to_db(token)

    #저장 위치를 입력합니다.
    address= '/Users/jisujung/Desktop/서울대/개인 공부/인턴_ETF/DB/'
    formula.to_csv(address + name+ '_formula.csv')
    stocks.to_csv(address + name+ '_stocks.csv')
    investment.to_csv(address + name+ '_investment.csv')
    financial.to_csv(address + name + '_financial.csv')


