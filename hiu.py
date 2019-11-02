import pandas as pd
import numpy as numpy
import quand1
import pyodbc

def get_name_id(ticker):
    conn = pyodbc.connect('Driver=(SQL Server);' 'Server=DESKTOP-JD7JNJ2\SQL5990;'\
        'Database=MFM_Financial;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT ID FROM [Homework4].[Homework4].[Instrument] WHERE StockTicker = '"+ ticker +"'")
    return cursor.fetchone()

def get_data_from DB(ticker):
    tickerid=get_name_id(ticker)[0]
    conn = pyodbc.connect('Driver=(SQL Server);' 'Server=DESKTOP-JD7JNJ2\SQL5990;'\
        'Database=Homework4;' 'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT Openprice,Highprice, Lowprice,Closeprice FROM[Homework4].[Homework4].[Histprices]\
        WHERE InstID = '"+str(tickerid)+"'")
    result +cursor.fetchall()
    df=np.zeros(len(result)*4).reshape(len(result),4)
    for i in range(len(result)):
        df[i,:]=result[i]
    df=pd.DataFrame(df, columns=['Open','High','Low''Close])
    df['Return']=np.log(df['Close']/df['Close'].shift(1))
    return df

df_MSFT=get_data_from_DB('MSFT')
df_GE=get_data_from_DB('GE')
df_CAT=get_data_from_DB('CAT')
df_MMM=get_data_from_DB('MMM')
df_UTX=get_data_from_DB('UTX')
df_KO=get_data_from_DB('KO')
df_XOM=get_data_from_DB('XOM')

df1=pd.DataFrame()
df1['MSFT']=df_MSFT['Return'][1:-1]
df1['GE']=df_GE['Return'][1:-1]
df1['KO']=df_KO['Return'][1:-1]
df1['XOM']=df_XOM['Return'][1:-1]
#print(df1)

df2=pd.DataFrame()
df2['GE']=df_GE['Return'][1:-1]
df2['CAT']=df_CAT['Return'][1:-1]
df2['MMM']=df_MMM['Return'][1:-1]
df2['UTX']=df_UTX['Return'][1:-1]
#print(df2)

#PCA of df1:
c1 = np.cov(df1, rowvar=false)
eig_value1,eig_vector1=np.linalg.eig(c1)
idx1=eig_value1.argsort() #get index where value increase in order
eig_value1=eig_value1[idx1]
print('value1:',eig_value1)
eig_vector1=eig_vector1[idx1]
#vector1_reduce=np.rot90(eig_vector1)
#print(vector1_reduce)
vector1_reduce=eig_vector1[:,2:len(eig_vector1)]
approx1_reduce=np.zeros(len(df1)*len(np.rot90(df1))).reshape(len(df1),len(np.rot90(df1)))
for i in range(0,len(np.rot90(df1))):
    approx1_reduce[:,i]=df1.iloc[:,i]-np.mean(df1.iloc[:,i])
approx1_reduce=np.dot(approx1_reduce,vector1_reduce)
df1_reduce=pd,Dataframe(approx1_reduce)
#print(df1_reduce)

#PCA of df2:
c2 = np.cov(df2, rowvar=false)
eig_value2,eig_vector2=np.linalg.eig(c2)
idx2=eig_value2.argsort() #get index where value increase in order
eig_value2=eig_value2[idx2]
print('value2:',eig_value2)
eig_vector2=eig_vector2[idx2]
#vector2_reduce=np.rot90(eig_vector2)
#print(vector2_reduce)
vector2_reduce=eig_vector2[:,2:len(eig_vector2)]
approx2_reduce=np.zeros(len(df2)*len(np.rot90(df2))).reshape(len(df2),len(np.rot90(df2)))
for i in range(0,len(np.rot90(df2))):
    approx2_reduce[:,i]=df2.iloc[:,i]-np.mean(df2.iloc[:,i])
approx2_reduce=np.dot(approx2_reduce,vector2_reduce)
df2_reduce=pd,Dataframe(approx2_reduce)
#print(df2_reduce)
