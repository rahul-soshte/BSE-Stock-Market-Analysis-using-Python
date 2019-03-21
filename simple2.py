import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import pandas as pd
from matplotlib import style
from sklearn import svm, preprocessing
import statistics
import pickle
from collections import Counter
style.use("ggplot")

how_much_better = 5

def Status_Calc(stock, sp500):
    difference = stock - sp500

    if difference > how_much_better:
        return 1
    else:
        return 0

features = ['Basic EPS (Rs.)',
    'Diluted EPS (Rs.)',
    'Cash EPS (Rs.)',
	'Book Value [ExclRevalReserve]/Share (Rs.)',
	'Book Value [InclRevalReserve]/Share (Rs.)',
	'Revenue from Operations/Share (Rs.)',
	'PBDIT/Share (Rs.)',
	'PBIT/Share (Rs.)',
	'PBT/Share (Rs.)',
	'Net Profit/Share (Rs.)',
	'PBDIT Margin (%)',
	'PBIT Margin (%)',	
	'PBT Margin (%)',	
	'Net Profit Margin (%)',
	'Return on Networth / Equity (%)',	
	'Return on Capital Employed (%)',
	'Return on Assets (%)',
	'Total Debt/Equity (X)',
	'Asset Turnover Ratio (%)',
	'Current Ratio (X)',
	'Quick Ratio (X)',		
	'Enterprise Value (Cr.)',
	'EV/Net Operating Revenue (X)',
	'EV/EBITDA (X)'
]

def Build_Data_Set():

    data_df = pd.read_csv("all_df.csv")

    # data_df = data_df[:100]
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace("NaN",0).replace("N/A",0)
    data_df=data_df.replace('inf',0)
    # data_df=data_df.dropna()
    
    data_df["Status2"] = list(map(Status_Calc, data_df["price_p_change"], data_df["sensex_p_change"]))

    X = np.array(data_df[features].values)

    y = (data_df["Status2"]
         .replace("underperform",0)
         .replace("outperform",1)
         .values.tolist())

    X = preprocessing.scale(X)
    
    Z = np.array(data_df[["price_p_change","sensex_p_change"]])

    return X,y,Z

def Analysis():
    test_size = 10

    X, y , Z= Build_Data_Set()
    print(len(X))

    clf = svm.SVC(kernel="linear", C= 1.0)
    clf.fit(X[:],y[:])
            
    data_df = pd.read_csv("forward.csv")

    # data_df = data_df.replace("N/A",0).replace("NaN",0)

    X = np.array(data_df[features].values)

    X = preprocessing.scale(X)

    Z = data_df["Code"].values.tolist()

    invest_list = []

    for i in range(len(X)):
        p = clf.predict(X[i].reshape(1,-1))[0]
        if p == 1:
            # print(Z[i])
            invest_list.append(Z[i])

    #print(len(invest_list))
    #print(invest_list)
    return invest_list

final_list = []

loops = 8

for x in range(loops):
    stock_list = Analysis()
    for e in stock_list:
        final_list.append(e)

x = Counter(final_list)

print(15*"_")
final_final_list=list()
for each in x:
    if x[each] > loops - (loops/3):
        print(each)
        final_final_list.append(each)





