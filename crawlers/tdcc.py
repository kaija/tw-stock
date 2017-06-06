import requests
import csv
from bs4 import BeautifulSoup

def get_tdcc_date(stock_id):
	date_list =[]
	url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	select = soup.find('select', attrs={'name':'SCA_DATE'})
	for row in select:
		for option in row:
			if option[0].isdigit:
				date_list.append(option)
	return date_list

def get_tdcc(stock_id, date_list):
	# for date_string in date_list:
	# 	url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=" + date_string + "&SqlMethod=StockNo&StockNo=" + stock_id + "&StockName=&sub=%ACd%B8%DF"
	# 	print url
	url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=" + date_list[1] + "&SqlMethod=StockNo&StockNo=" + stock_id + "&StockName=&sub=%ACd%B8%DF"
	print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	table = soup.findAll('table', attrs={'cellspacing':'0', 'cellpadding':'0', 'width':"100%", 'border':'1', 'class':"mt", 'bordercolor':"#B0CAFF"})
	for row in table[1].findAll("tr"):
		tds = row.findAll("td")
		if tds[0].contents[0].isdigit():
			print "range:", tds[1].contents[0]
			print "population:", tds[2].contents[0]
			print "stock number:", tds[3].contents[0]
			print "portion:", tds[4].contents[0]
			print "============="



date_list = get_tdcc_date(stock_id='2337')
get_tdcc('2337', date_list)