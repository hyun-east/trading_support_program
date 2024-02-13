import numpy as np
from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
st1 = input('첫번째 종목의 종목코드를 입력하십시오')
st2 = input('두번째 종목의 종목코드를 입력하십시오')
st3 = input('세번째 종목의 종목코드를 입력하십시오')
st4 = input('네번째 종목의 종목코드를 입력하십시오')
yf.pdr_override()
stocks = [st1, st2, st3, st4]
df = pd.DataFrame()
for s in stocks:
    ps = pdr.get_data_yahoo(s, start='2015-05-04')
    df[s]=ps.Close

daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252

port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []

for _ in range(50000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns/risk)

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]

max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]
min_risk = df.loc[df['Risk'] == df['Risk'].min()]

df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
    edgecolors='k', figsize=(11,7), grid=True)
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r',
    marker='*', s=300)
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r',
    marker='X', s=200)
print(max_sharpe)
print(min_risk)
plt.title('Portfolio Optimization')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()
input()