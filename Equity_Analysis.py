'''
Andrew Antczak -- July 14th, 2020

This code is intended to produce an excel sheet organizing financial data for a random assortment of companies.
'''

import numpy as np
from iexfinance.stocks import Stock
import os
import pandas as pd
#-----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# SETTING UP IEX CLOUD API ENVIRONMENT

#REAL IEX_TOKEN
IEX_TOKEN = "API_TOKEN_HERE"

'''
IF BELOW IS GRAY THEN YOU'RE USING THE REAL TOKEN FROM ABOVE. 

These tokens allow access to IEX's data. This is something
you'll get used to doing regardless of the service you're using. It's how they connect your requests to your account.

A nice feature is the sandbox token below. This allows you to pull "scrambled" data from their service such that you can 
sanity check your code. You never want to pull real data without checking your code's ability to function properly. 

An example of this is the following: I was running a data pull on the entire NYSE. Small amounts of data per company, but
a lot of data overall, it equated to roughly $50. When the code was done running, there was a small syntax error on the output 
end of things. Guess what? None of the data saved. $50 for nothing. Don't let that happen to you!
'''
# Sandbox Testing API Token
#IEX_TOKEN = "SANDBOX_API_TOKEN_HERE"

# This indicates that is is sandbox testing so iex cloud can access. Comment out if you're using for non-testing.
#os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
# ----------------------------------------------------------------------------------------------------------------------

tickers = ['AAPL', 'AMZN', 'FB', 'GOOG', 'MSFT', 'BA', 'NFLX', 'DIS', 'ZM', 'RVP']

sector = []
industry = []
mc = []
pe_ratio = []
price = []
price_target = []
pct_change_1m = []
pct_change_ytd = []
avg30_volume = []
cash_flow = []
tdebt_to_casset = []
casset_to_cdebt = []
n_income = []
tickers_f = []

start = '2019-06-01'
end = '2020-07-14'
for i, ticker in enumerate(tickers):
    ticker = ticker.replace(" ", "")
    stock = Stock(ticker.replace("-", "."), token=IEX_TOKEN)
    tickers_f.append(ticker)
    print(ticker.replace("-", "."))
    try:
        sector.append(stock.get_company()['sector'])
    except:
        sector.append(np.nan)
    try:
        industry.append(stock.get_company()['industry'])
    except:
        industry.append(np.nan)
    try:
        mc.append(float(stock.get_market_cap()))
    except:
        mc.append(np.nan)
    try:
        pe_ratio.append(stock.get_key_stats()['peRatio'])
    except:
        pe_ratio.append(np.nan)
    try:
        price.append(stock.get_price())
    except:
        price.append(np.nan)
    try:
        price_target.append(stock.get_price_target()['priceTargetAverage'])
    except:
        price_target.append(np.nan)
    try:
        pct_change_1m.append(stock.get_key_stats()['month1ChangePercent'])
    except:
        pct_change_1m.append(np.nan)
    try:
        pct_change_ytd.append(stock.get_key_stats()['ytdChangePercent'])
    except:
        pct_change_ytd.append(np.nan)
    try:
        avg30_volume.append(stock.get_key_stats()['avg30Volume'])
    except:
        avg30_volume.append(np.nan)
    try:
        pos = 0
        neg = 0
        for period in stock.get_cash_flow(last=8)['cashflow']:
            try:
                if float(period['cashFlow']) > 0.0:
                    pos += 1
                if float(period['cashFlow']) < 0.0:
                    neg += 1
            except:
                pass
        try:
            cash_flow.append(str(pos) + " positive quarters; " + str(neg) + " negative quarters.")
        except:
            print("Fail")
            cash_flow.append(np.nan)
    except:
        cash_flow.append(np.nan)
    try:
        financials = stock.get_financials(last=1)[0]
        tratio = float(financials['totalDebt'])/float(financials['currentAssets'])
        tdebt_to_casset.append(tratio)
    except:
        tdebt_to_casset.append(np.nan)
    try:
        cratio = float(financials['currentAssets'])/float(financials['currentDebt'])
        casset_to_cdebt.append(cratio)
    except:
        casset_to_cdebt.append(np.nan)
    try:
        n_income.append(stock.get_income_statement()[0]['netIncome'])
    except:
        n_income.append(np.nan)

FS = pd.DataFrame({'Sector': sector, 'Industry': industry, 'Market_Cap': mc, 'PE_Ratio': pe_ratio, 'Price': price,
                   'Price_Target': price_target, '1M_Pct_Change': pct_change_1m, 'YTD_Pct_Change': pct_change_ytd,
                   'Avg_30D_Volume': avg30_volume, 'Cash_Flow': cash_flow, 'Total Debt to Asset Ratio': tdebt_to_casset,
                   'Current Asset to Debt Ratio': casset_to_cdebt, 'Net_Income': n_income},
                  columns=['Sector', 'Industry', 'Market_Cap', 'PE_Ratio', 'Price', 'Price_Target', '1M_Pct_Change',
                           'YTD_Pct_Change', 'Avg_30D_Volume', 'Cash_Flow', 'Total Debt to Asset Ratio',
                           'Current Asset to Debt Ratio', 'Net_Income'],
                  index=tickers_f)

FS.to_excel('Equity_Analysis.xlsx')

