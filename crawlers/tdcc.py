import os, csv, requests, sys, datetime
import pandas as pd
from bs4 import BeautifulSoup

def get_tdcc_date(stock_id, exist_file_list):
	date_list =[]
	url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	select = soup.find('select', attrs={'name':'SCA_DATE'})
	for row in select:
		for option in row:
			if option.isdigit():
				date_list.append(option)

	base_date='empty'
	old_file_name = None
	for file_name in exist_file_list:
	    if file_name.startswith(stock_id):
	    	old_file_name = file_name
	        base_date = file_name.split('_')[1].split('.')[0]
	        break
	if base_date =='empty':
		base_date = '19000101'	
	base_date_covert = datetime.datetime.strptime(base_date, "%Y%m%d").date()

	new_date_list = []
	for date in date_list:
		date_convert = datetime.datetime.strptime(date, "%Y%m%d").date()
		if date_convert > base_date_covert:
			new_date_list.append(date)
	return new_date_list, old_file_name

def get_tdcc(stock_id, date_list):
    data = []
    for date_string in date_list:
        url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=" + date_string + "&SqlMethod=StockNo&StockNo=" + stock_id + "&StockName=&sub=%ACd%B8%DF"        
        res = requests.get(url)
        if res.status_code != 200:
        	continue;
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.findAll('table', attrs={'cellspacing':'0', 'cellpadding':'0', 'width':"100%", 'border':'1', 'class':"mt", 'bordercolor':"#B0CAFF"})
        try:
        	for row in table[1].findAll("tr"):
	            tds = row.findAll("td")
	            if tds[0].contents[0].isdigit():
	                date_data=[]
	                date_data.append("{}_{}".format(date_string, tds[1].contents[0]))
	                date_data.append(tds[2].contents[0]) 
	                date_data.append(tds[3].contents[0])
	                date_data.append(tds[4].contents[0])
	#                 print "range:", tds[1].contents[0]
	#                 print "population:", tds[2].contents[0]
	#                 print "stock number:", tds[3].contents[0]
	#                 print "portion:", tds[4].contents[0]
	#                 print "============="
	                data.append(date_data)
        except IndexError:
        	# print "this request is no data, skip"
        	break
    df_data = pd.DataFrame(data, columns=['date_level', 'population', 'stock number', 'total portion'])
    return df_data
	

def get_all_stockid(data_path): 
	stock_list = []
	for file_name in os.listdir(data_path):
		stock_id = file_name.split('.csv')[0]
		stock_list.append(stock_id)
	return stock_list

reload(sys)
sys.setdefaultencoding('utf-8')

exist_file_list = os.listdir('tdcc/')
stock_list = get_all_stockid('bystock/')
# stock_list = ['0015', '0050']

for stock_id in stock_list:
	try:
		date_list, old_file_name = get_tdcc_date(stock_id=stock_id, exist_file_list=exist_file_list)
		new_df_data = get_tdcc(stock_id=stock_id, date_list=date_list)
	
		if len(date_list) == 0 :
			# print stock_id, "no need to update"
			continue
		elif old_file_name == None:
			new_file_name = "{}_{}.csv".format(stock_id, date_list[0] if len(new_df_data)>0 else 'empty')
			new_df_data.to_csv("tdcc/{}".format(new_file_name), sep=',', index=False, encoding='utf-8')
			# print new_file_name, "csv file created"
		else:
			orig_df = pd.read_csv('tdcc/{}'.format(old_file_name))
			df = pd.concat([new_df_data, orig_df])		
			new_file_name = "{}_{}.csv".format(stock_id, date_list[0] if len(df)>0 else 'empty')		
			os.rename('tdcc/{}'.format(old_file_name), 'tdcc/{}'.format(new_file_name))		
			df.to_csv("tdcc/{}".format(new_file_name), sep=',', index=False, encoding='utf-8')
			# print new_file_name, "added {} data".format(len(new_df_data))
	except:
		print stock_id, "get error"
		continue

