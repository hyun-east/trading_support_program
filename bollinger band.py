import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
codename = input('종목코드를 입력하십시오')
startdate = input('시작일자를 입력하십시오')
df = pdr.get_data_yahoo( codename, start=startdate)
dfc = df.Close

df['MA20'] = dfc.rolling(window=20).mean()  # ①
df['stddev'] = dfc.rolling(window=20).std()  # ②
df['upper'] = df['MA20'] + (df['stddev'] * 2)  # ③
df['lower'] = df['MA20'] - (df['stddev'] * 2)  # ④
plt.figure(figsize=(9, 5))
plt.plot(df.index, dfc, color='#0000ff', label='Close')  # ⑥
plt.plot(df.index, df['upper'], 'r--', label='Upper band')  # ⑦
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  # ⑧
plt.legend(loc='best')
plt.title('Bollinger Band (20 day, 2 std)')
plt.show()
input()