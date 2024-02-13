while True:
    qwer = int(input('효율적투자곡선 : 1\n선형회귀분석   : 2\n볼린저밴드     : 3\n원하는 기능을 선택하십시오: '))
    if qwer == 1:
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
            df[s] = ps.Close

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
            sharpe_ratio.append(returns / risk)

        portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
        for i, s in enumerate(stocks):
            portfolio[s] = [weight[i] for weight in port_weights]
        df = pd.DataFrame(portfolio)
        df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]

        max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]
        min_risk = df.loc[df['Risk'] == df['Risk'].min()]

        df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
                        edgecolors='k', figsize=(11, 7), grid=True)
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

    if qwer == 2:
        import pandas as pd
        from pandas_datareader import data as pdr
        import yfinance as yf

        yf.pdr_override()
        from scipy import stats
        import matplotlib.pylab as plt

        a = input('첫번째 코드를 입력하십시오')
        b = input('두번째 코드를 입력하십시오')
        c = input('시작일을 입력하십시오')
        k = a + b
        dow = pdr.get_data_yahoo(a, c)
        kospi = pdr.get_data_yahoo(b, c)

        df = pd.DataFrame({'X': dow['Close'], 'Y': kospi['Close']})
        df = df.fillna(method='bfill')
        df = df.fillna(method='ffill')

        regr = stats.linregress(df.X, df.Y)
        regr_line = f'Y = {regr.slope:2f}  X + {regr.intercept:2f}'
        print(regr)

        plt.figure(figsize=(7, 7))
        plt.plot(df.X, df.Y, '.')
        plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
        plt.legend([k, regr_line])
        plt.title(f'liner regression (R = {regr.rvalue:2f})')
        plt.xlabel(a)
        plt.ylabel(b)
        plt.show()
        input()
    if qwer == 3:
        import matplotlib.pyplot as plt
        import yfinance as yf
        from pandas_datareader import data as pdr

        yf.pdr_override()
        codename = input('종목코드를 입력하십시오')
        startdate = input('시작일자를 입력하십시오')
        df = pdr.get_data_yahoo(codename, start=startdate)
        dfc = df.Close

        df['MA20'] = dfc.rolling(window=20).mean()
        df['stddev'] = dfc.rolling(window=20).std()
        df['upper'] = df['MA20'] + (df['stddev'] * 2)
        df['lower'] = df['MA20'] - (df['stddev'] * 2)
        plt.figure(figsize=(9, 5))
        plt.plot(df.index, dfc, color='#0000ff', label='Close')
        plt.plot(df.index, df['upper'], 'r--', label='Upper band')
        plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
        plt.plot(df.index, df['lower'], 'c--', label='Lower band')
        plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
        plt.legend(loc='best')
        plt.title('Bollinger Band (20 day, 2 std)')
        plt.show()
        input()
