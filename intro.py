import pandas as pd
import quandl

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High','Adj. Low','Adj. Close','Adj. Volume']]

df['HL_PCT'] = (df['Adj. High']-df['Adj. Close'])/ df['Adj. Close'] #Margin of volatility

df['PCT_change'] = (df['Adj. Close']-df['Adj. Open'])/ df['Adj. Open'] #Margin of old vs new

df = df[['Adj. Close', 'HL_PCT','PCT_change','Adj. Volume']] #Volume: How many sales were made