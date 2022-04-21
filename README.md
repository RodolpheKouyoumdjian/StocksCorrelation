# StocksCorrelation
A program that will return the Pearson correlation coefficient of the stocks entered. One coefficient is returned for each possible pair. The program will plot a heat map and will return a CSV file containing the correlation of each possible stock pair.

Line 12 & 13: Start and end date of data used to calculate the Pearson correlation coefficient.
Line 70: Set the annot parameter to True if you want the correlation coefficients to be written on the heatmap, False in the opposite case.

If you wish to change the dates or remove/add stocks, restart the program. 

In the tickers.txt textfile, write one stock symbol per line. The stock symbol of the company should be the same as the ones written on finance.yahoo.com

Libraries used:
pandas,
numpy,
scipy,
datetime,
seaborn,
matplotlib.pyplot,
yfinance,
warnings,

The file Stocks_correlations_by_industry.ipynb was added as a follow up to the initial idea. The code for the basic tool was improved and an analysis concerning the results was conducted. See bottom of file for conclusions. 
