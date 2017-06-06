from selenium import webdriver
from bs4 import BeautifulSoup


def stock_dist(stock_id):
    data = []

    url = 'http://goodinfo.tw/StockInfo/EquityDistributionClassHis.asp?STOCK_ID='+stock_id+'&DISPLAY_CAT=SHAREHOLD_RATIO&CHT_CAT=WEEK'
    driver = webdriver.PhantomJS(executable_path='/opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get(url)
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'lxml')
    table = soup.find('table', attrs={'class':'solid_1_padding_3_0_tbl'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    return data


data = stock_dist(stock_id='2337')
print data
