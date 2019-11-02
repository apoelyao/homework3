import pandas as pd
import numpy as numpy
import quand1
import pyodbc

#adding tickers to the instrument table
def add_name(company, ticker, market, sector):
    conn = pyodbc.connect('Driver=(SQL Server);' 'Server=DESKTOP-JD7JNJ2\SQL5990;'\
        'Database=MFM_Financial;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO [Homework4].[Homework4].[Instrument] VALUES \
        ('"+ company +"','"+ ticker +"','"+ market +"','"+ sector +"')")
    conn.commit()
add_name('Microsoft','MSFT','NASDAQ','Technology')
add_name('General Eletric','GE','NYSE','Industrial Goods')
add_name('Caterpillar Inc','CAT','NYSE','Industrial Goods')
add_name('3M company','MMM','NYSE','Industrial Goods')
add_name('United technologies','UTX','NYSE','Industrial Goods')
add_name('Coca-cola','KO','NYSE','Consumer Goods')
add_name('Exxon Mobile Corporation','XOM','NYSE','Basic Material')

ticket_set=['MSFT', 'GE', 'CAT', 'MMM', 'UTX', 'KO', 'XOM']

def get_name_id(ticker):
    conn = pyodbc.connect('Driver=(SQL Server);' 'Server=DESKTOP-JD7JNJ2\SQL5990;'\
        'Database=MFM_Financial;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT ID FROM [Homework4].[Homework4].[Instrument] WHERE StockTicker = '"+ ticker +"'")
    return cursor.fetchone()
#print(get_name_id('KO'))

def add_timeseries_from_quandl(ticker)：
    tickerid = get_name_id(ticker)[0]
    conn = pyodbc.connect('Driver=(SQL Server);' 'Server=DESKTOP-JD7JNJ2\SQL5990;'\
        'Database=Homework4;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

    quandl.Apiconfig.api_key='' #API key

    df=pd.DaraFrame(quandl.get('EOD/'+ticker))
    df=df.reset_index()
    for i in range(len(df)):
        cursor.execute("INSERT INTO [Homework4].[Homework4].[HistPrice] VALUES ('"+ str(tickerid)+"',\
            '"+str(df.iloc[i]['Date'])+"','"+str(df.iloc[i]['open'])+"',\
            '"+str(df.iloc[i]['High'])+"','"+str(df.iloc[i]['low'])+"',\
            '"+str(df.iloc[i]['close'])+"','"+str(df.iloc[i]['Volume']))+"')")
    conn.commit()

def populate(ticker_set):
    for ticker in ticker_set:
        add_timeseries_from_quandl(ticker)

populate(ticker_set)
    
