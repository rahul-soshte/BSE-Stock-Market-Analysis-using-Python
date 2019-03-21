import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime
import csv
from operator import itemgetter

# '500325','500096
listofcomps = ['530007','532644','500325','500096']

dates=['31-March-2014','31-March-2015','31-March-2016','31-March-2017','28-March-2018']
def download_data_of_stock():
	source = pd.read_html("https://www.moneycontrol.com/financials/relianceindustries/ratiosVI/RI#RI")
	print(source)
	df = source[2][5:]
	df.columns=['Ratio','Mar18','Mar17','Mar16','Mar15','Mar14']
	df.to_csv("bse/500325.csv")

download_data_of_stock()

def seperate_dataset_single_14(stock):
	df=pd.read_csv('bse/{}.csv'.format(str(stock)))
	df.drop(['Mar18','Mar17','Mar16','Mar15'],1,inplace=True)
	df=df.drop(df.columns[[0]],axis=1)
	df.rename(columns={'Mar14':dates[0]},inplace=True)
	df=df.T
	try:
		df = df.drop(df.columns[[11,21,29,38,39,40,41,42]],axis=1)
	except:
		df= df.drop(df.columns[[10,20,23,31,32,33,34,35]],axis=1)
	df.to_csv("bse/{}_{}.csv".format(str(stock),'14'))

def seperate_dataset_single_15(stock):
	df=pd.read_csv('bse/{}.csv'.format(str(stock)))
	df.drop(['Mar18','Mar17','Mar16','Mar14'],1,inplace=True)
	df=df.drop(df.columns[[0]],axis=1)
	df.rename(columns={'Mar15':dates[1]},inplace=True)
	df=df.T
	try:
		df = df.drop(df.columns[[11,21,29,38,39,40,41,42]],axis=1)
	except:
		df= df.drop(df.columns[[10,20,23,31,32,33,34,35]],axis=1)
	df.to_csv("bse/{}_{}.csv".format(str(stock),'15'))

def seperate_dataset_single_16(stock):
	df=pd.read_csv('bse/{}.csv'.format(str(stock)))
	df.drop(['Mar18','Mar17','Mar15','Mar14'],1,inplace=True)
	df=df.drop(df.columns[[0]],axis=1)
	df.rename(columns={'Mar16':dates[2]},inplace=True)
	df=df.T
	try:
		df = df.drop(df.columns[[11,21,29,38,39,40,41,42]],axis=1)
	except:
		df= df.drop(df.columns[[10,20,23,31,32,33,34,35]],axis=1)
	df.to_csv("bse/{}_{}.csv".format(str(stock),'16'))


def seperate_dataset_single_17(stock):
	df=pd.read_csv('bse/{}.csv'.format(str(stock)))
	df.drop(['Mar18','Mar16','Mar15','Mar14'],1,inplace=True)
	df=df.drop(df.columns[[0]],axis=1)
	df.rename(columns={'Mar17':dates[3]},inplace=True)
	df=df.T
	try:
		df = df.drop(df.columns[[11,21,29,38,39,40,41,42]],axis=1)
	except:
		df= df.drop(df.columns[[10,20,23,31,32,33,34,35]],axis=1)
	df.to_csv("bse/{}_{}.csv".format(str(stock),'17'))	

def seperate_dataset_single_18(stock):
	df=pd.read_csv('bse/{}.csv'.format(str(stock)))
	df.drop(['Mar17','Mar16','Mar15','Mar14'],1,inplace=True)
	df=df.drop(df.columns[[0]],axis=1)
	df.rename(columns={'Mar18':dates[4]},inplace=True)
	df=df.T
	try:
		df = df.drop(df.columns[[11,21,29,38,39,40,41,42]],axis=1)
	except:
		df= df.drop(df.columns[[10,20,23,31,32,33,34,35]],axis=1)
	df.to_csv("bse/{}_{}.csv".format(str(stock),'18'))

def seperation():
	for code in listofcomps:
		seperate_dataset_single_14(code)
		seperate_dataset_single_15(code)
		seperate_dataset_single_16(code)
		seperate_dataset_single_17(code)
		seperate_dataset_single_18(code)

seperation()

def combine():
	for code in listofcomps:
		df=pd.read_csv('bse/'+str(code)+"_14.csv")
		df1=pd.read_csv('bse/'+str(code)+"_15.csv")
		df2=pd.read_csv('bse/'+str(code)+"_16.csv")
		df3=pd.read_csv('bse/'+str(code)+"_17.csv")
		df4=pd.read_csv('bse/'+str(code)+"_18.csv")
		concat=pd.concat([df,df1[1:],df2[1:],df3[1:],df4[1:]])
		concat.columns = df.iloc[0]
		# print(conc)
		concat.to_csv('bse/concatanated_{}.csv'.format(str(code)))

combine()

# https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?scripcode=512289&flag=sp&Submit=G

def get_data_from_bseindia(bsecodes=[]):
	if not os.path.exists('bse_stock_data'):
		os.makedirs('bse_stock_data')

	fp=webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList",2)
	fp.set_preference("browser.download.dir",'/home/hunter/fund_analysis_bse/bse_stock_data')
	driver=webdriver.Firefox(firefox_profile=fp)
	for code in bsecodes:
		if not os.path.exists('bse_stock_data/{}.csv'.format(code)):
			try:
				driver.get("https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?scripcode="+code+"&flag=sp&Submit=G")
					
				elem=driver.find_element_by_id('ContentPlaceHolder1_txtFromDate')
				elem.clear()
				elem=driver.find_element_by_css_selector(".ui-datepicker-year")
				elem.click()
				elem=driver.find_element_by_css_selector('.ui-datepicker-year > option:nth-child(5)')
				elem.click()
				elem=driver.find_element_by_css_selector(".ui-datepicker-month")
				elem.click()
				elem=driver.find_element_by_css_selector('.ui-datepicker-month > option:nth-child(2)')
				elem.click()
				
				elem=driver.find_element_by_link_text('10')
				elem.click()
				button=driver.find_element_by_id("ContentPlaceHolder1_btnSubmit")
				button.click()
				elem=driver.find_element_by_css_selector("#ContentPlaceHolder1_btnDownload1 > .fa")
				elem.click()
			except:
				print("Not found {}".format(code))
				pass
		else:
			print("Already have {}".format(code))	
	try:
		driver.close()
	except:
		print("Driver already closed")

get_data_from_bseindia(listofcomps)

def sortacctodate():

	for code in listofcomps:
		rows=[]
		df=pd.read_csv("bse_stock_data/{}.csv".format(code))
		df.set_index("Date",inplace=True)
		df.rename(columns={"Close Price":code},inplace=True)
		df.drop(['Open Price',
			'High Price',
			'Low Price','WAP',
			'No.of Shares'
			,'No. of Trades',
			'Total Turnover (Rs.)',
			'Deliverable Quantity',
			'% Deli. Qty to Traded Qty',
			'Spread High-Low',
			'Spread Close-Open'],1,inplace=True)
		df.to_csv("bse_stock_data/close_{}.csv".format(code))
		with open('bse_stock_data/close_{}.csv'.format(code),'r') as f:
			reader=csv.reader(f,delimiter=',')
			header=next(reader)
			for row in reader:
				row[0] = datetime.strptime(row[0],"%d-%B-%Y")
				rows.append(row)
		rows.sort(key=itemgetter(0))
		f1=csv.writer(open("sorted_{}_dates.csv".format(code),'w'))
		f1.writerow(header)
		for row in rows:
			row[0]=row[0].strftime('%d-%B-%Y')
			f1.writerow(row)

sortacctodate()

def process_data_for_labels():
	main_df=pd.DataFrame()
	forward_sample_df = pd.DataFrame()  
	for code in listofcomps:
		df=pd.read_csv('bse/concatanated_{}.csv'.format(code),index_col=0)
		data2=pd.read_csv('sorted_{}_dates.csv'.format(code))
		data3=pd.read_csv("SENSEX.csv",index_col=False)

		df=pd.merge(df,data2,left_on=['Ratio'],right_on=["Date"],how='inner')
		df=df.merge(data3,on="Date",how='inner')
		df.drop(['Date','Open','High','Low'],1,inplace=True)
		df['Code']=[code]*len(df)
		data =df[code].values.tolist()
		data4=df['Close'].values.tolist()

		count_row = df.shape[0]
		price_p_change = list()
		sensex_p_change =list()
		diff = list()
		status = list()

		for i in range(0, count_row-1):
			price_p_change.append(((data[i+1]-data[i])/data[i])*100)
			sensex_p_change.append(((data4[i+1]-data4[i])/data4[i])*100)
			diff.append(price_p_change[i]-sensex_p_change[i])
			if(diff[i] > 0):
				status.append('outperform')
			else:
				status.append('underperform')

		sensex_p_change.append(0.0)
		price_p_change.append(0.0)
		status.append('To be predicted')

		df['price_p_change']=price_p_change
		df['sensex_p_change']=sensex_p_change
		df['Status'] = status

		if forward_sample_df.empty:
			forward_sample_df=df[4:]
		else:
			forward_sample_df = pd.concat([forward_sample_df,df[4:]],sort=False)

		if main_df.empty:
			main_df = df[:-1]
		else:
			main_df = pd.concat([main_df,df[:-1]],sort=False)

	return main_df,forward_sample_df

all_df,forward_df = process_data_for_labels()
all_df.to_csv('all_df.csv')
forward_df.to_csv('forward.csv')

# process_data_for_labels()

















































seperate_dataset_single_14(530007)