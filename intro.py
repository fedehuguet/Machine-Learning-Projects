import pandas as pd
import quandl
import math

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High','Adj. Low','Adj. Close','Adj. Volume']]

df['HL_PCT'] = (df['Adj. High']-df['Adj. Close'])/ df['Adj. Close']*100 #Margin of volatility

df['PCT_change'] = (df['Adj. Close']-df['Adj. Open'])/ df['Adj. Open']*100 #Margin of old vs new

df = df[['Adj. Close', 'HL_PCT','PCT_change','Adj. Volume']] #Volume: How many sales were made

forecast_col = 'Adj. Close'
df.fillna(-9999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df))) #Try to predict out of 1% of the data, 10 days in the future aprox.
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)
print(df.head())