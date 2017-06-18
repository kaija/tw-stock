import os
import pandas as pd
for file_name in os.listdir(os.getcwd()):
    if file_name.endswith('.csv'):
    	stock_id = file_name.split('_')[0]
        df = pd.read_csv(file_name)
        new_file_name = '{}_{}.csv'.format(stock_id, df.loc[0]['date_level'].split('_')[0]) if len(df) > 0 else '{}_empty.csv'.format(stock_id)        
        os.rename(file_name, new_file_name)        
        print file_name, new_file_name