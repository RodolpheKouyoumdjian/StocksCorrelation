import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

def StockCorrs():
    StartDate = '2020-01-01'
    EndDate = '2021-01-01'

    start_time = datetime.now() # To get program execution time

    # Creating a list of all stock symbols
    text_file = np.array([open('tickers.txt', 'r').readlines()])
    stocks = np.char.strip(text_file, '\n')
    stocks = np.unique(stocks).tolist()
    nstocks = len(stocks) # Number of stocks
    data = np.array([])  # Will contain stock % change
    opens = yf.download(tickers=stocks, start=StartDate, end=EndDate)['Open'] #Data frame of all open prices

    # Creating an array that will contain all daily changes
    for ticker in stocks:
        sprice = np.array(opens[ticker])
        for index in range(len(sprice)-1, 0, -1):  # Convert to daily percent change
            sprice[index] = sprice[index]/sprice[index-1]
        sprice = np.delete(sprice, 0)
        data = np.append(data, sprice) #Add the stock's data to the array of total data

    data = data[~np.isnan(data)]
    data = data.reshape(nstocks, int(len(data)/nstocks))

    # Correlation data & name of pairs data
    correlation, names = np.array([]), np.array([])

    for ticker1 in range(nstocks): #Iterate through first stock of the pair
        stock1 = data[ticker1] #Array containing % change of stock 1

        for ticker2 in range(ticker1+1, nstocks): #Iterate for second stock of the pair
            names = np.append(names, stocks[ticker1] + '/' + stocks[ticker2])
            #Add the correlation to the correlation array
            correlation = np.append(correlation, pearsonr(stock1, data[ticker2])[0])

    # Table containing the data that will be transferred to the CSV
    corr_table = np.concatenate((correlation, names)).reshape(2, len(correlation)).T
    corr_table = corr_table[corr_table[:,0].argsort()][::-1]

    # Transfer data table to CSV
    df = pd.DataFrame(corr_table)
    df.to_csv('Pairs correlation.csv')

    # Formatting the data to create a heatmap
    HeatData = np.array([])
    length = np.linspace(1, nstocks - 1, nstocks - 1)[::-1]
    indices = np.insert(length.cumsum(), 0, 0)

    for i in range(1, len(indices)):
        arr = correlation[int(indices[i-1]):int(indices[i])].tolist()
        arr = arr[::-1]
        while len(arr) != nstocks:
            arr.append(0)
        HeatData = np.insert(HeatData, 0, arr)
    HeatData = np.insert(HeatData, 0, np.zeros(nstocks))
    HeatData = np.reshape(HeatData, (nstocks, nstocks))

    mask = np.triu(np.ones_like(HeatData, dtype=bool))
    HeatMap = sns.heatmap(HeatData, mask=mask, xticklabels=stocks[1:][::-1], yticklabels=stocks[::-1], cmap='rocket_r', annot=True)
    plt.axes().set_title('Correlation heatmap')
    end_time = datetime.now()
    print(str(int(nstocks*(nstocks-1)/2)) + ' pairs were correlated in ' + str(end_time-start_time))

    plt.show()

try:
    StockCorrs()
except:
    print('Something went wrong, please try again!')
    StockCorrs()