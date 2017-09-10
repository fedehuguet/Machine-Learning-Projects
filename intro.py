import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High','Adj. Low','Adj. Close','Adj. Volume']]

df['HL_PCT'] = (df['Adj. High']-df['Adj. Close'])/ df['Adj. Close']*100 #Margin of volatility

df['PCT_change'] = (df['Adj. Close']-df['Adj. Open'])/ df['Adj. Open']*100 #Margin of old vs new

df = df[['Adj. Close', 'HL_PCT','PCT_change','Adj. Volume']] #Volume: How many sales were made

forecast_col = 'Adj. Close'
df.fillna(-9999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df))) #Try to predict out of 1% of the data, 10 days in the future aprox.
print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

x = np.array(df.drop(['label'],1))
y = np.array(['label'])
x = preprocessing.scale(x)
y = np.array(df['label'])

x_train, x_test, y_train, y_test = cross_validation.train_test_split(x,y,test_size=0.2)

clf = LinearRegression()
#clf = svm.SVR()
clf.fit(x_train, y_train)
accuracy = clf.score(x_test, y_test)
print(accuracy)