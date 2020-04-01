# -*- coding: utf-8 -*-
import yfinance as yf
import matplotlib.pyplot as plt

ticker = "GGAL.BA"
data = yf.download(ticker,period='20y')

print(data.head(4))
print('\n--Describe--\n', data.describe())
print('\n--Columns--\n', data.columns)
"""
plt .style.use('dark_background')
plt.rcParams['figure.figsize'] = [12.0, 5]
plt.yscale('log')
data['Adj Close'].plot(kind='line',title='GGAL en pesos')

variaciones =  data['Adj Close'].pct_change()*100

agrupados = variaciones.groupby(data.index.year).sum()
agrupados.plot(kind='bar',title='GGAL - Suma de Rendimientos/año')
plt .show()

agrupados = variaciones.groupby(data.index.dayofweek).mean()
agrupados.plot(kind='bar',title='GGAL - Rendimientos/Dia Semana')
plt .show()

data['Adj Close'].resample('W').last() 
variaciones =  data['Adj Close'].pct_change()*100
agrupados = variaciones.groupby(data.index.week).mean()
agrupados.plot(kind='bar',title='GGAL- Rendimientos/Semana del Año')
plt .show()

"""