import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from scipy import stats
import matplotlib.pylab as plt
a = input('첫번째 코드를 입력하십시오')
b = input('두번째 코드를 입력하십시오')
c = input('시작일을 입력하십시오')
k = a+ b
dow = pdr.get_data_yahoo(a, c)
kospi = pdr.get_data_yahoo(b, c)

df = pd.DataFrame({'X':dow['Close'], 'Y':kospi['Close']})
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:2f}  X + {regr.intercept:2f}'

plt.figure(figsize=(7, 7))
plt.plot(df.X, df.Y, '.')
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
plt.legend([k, regr_line])
plt.title(f'liner regression (R = {regr.rvalue:2f})')
plt.xlabel(a)
plt.ylabel(b)
plt.show()