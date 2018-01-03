#Predicts next 30 days of prices
import pandas as pd
import quandl
import math
import datetime
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High','Adj. Low','Adj. Close','Adj. Volume']]

df['HL_PCT'] = (df['Adj. High']-df['Adj. Low'])/ df['Adj. Low']*100 #Margin of volatility

df['PCT_change'] = (df['Adj. Close']-df['Adj. Open'])/ df['Adj. Open']*100 #Margin of old vs new

df = df[['Adj. Close', 'HL_PCT','PCT_change','Adj. Volume']] #Volume: How many sales were made

forecast_col = 'Adj. Close'
df.fillna(-9999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df))) #Try to predict out of 1% of the data.
print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out)

x = np.array(df.drop(['label'],1))
x = preprocessing.scale(x)
x_lately = x[-forecast_out:]
x = x[:-forecast_out]

df.dropna(inplace=True)
y = np.array(['label'])
y = np.array(df['label'])

x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y,test_size=0.2)

clf = LinearRegression(n_jobs=-1)
#clf = svm.SVR()
clf.fit(x_train, y_train)
accuracy = clf.score(x_test, y_test)
#print(accuracy)
forecast_set = clf.predict(x_lately) #Build prediction using classifier

print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
#last_unix = last_date.timestamp()
last_unix = (last_date - datetime.datetime(1970,1,1)).total_seconds()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix += one_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()