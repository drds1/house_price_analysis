import numpy as np
import pandas as pd
import matplotlib.pylab as plt





#df = pd.read_csv('./data/burton_joyce_data.csv')
#data ingestion Data from hm land registry
#https://landregistry.data.gov.uk/\
df = pd.read_csv('./data/all_notts.csv')

cols = ['price_paid',
        'deed_date',
        'postcode',
        'property_type',
        'new_build',
        'estate_type',
        'locality',
        'town',
        'district',
        'county',
        'transaction_category']

df = df[cols]
df['deed_date'] = pd.to_datetime(df['deed_date'])
#isolate burton joyce
dfbj = df[df['locality']=='BURTON JOYCE']

#groupby sale date monthly cadence
def group_houseprice(df,datecol='deed_date',val='price_paid',cadence='M',runningavg=3):
    df[datecol] = df[datecol].dt.to_period(cadence)
    dfagg = df[[datecol, val]].groupby(datecol).quantile([0.25, 0.5, 0.75]).reset_index()
    dfagg.columns = [datecol, 'quantile', val]
    dfagg.sort_values(by=datecol, inplace=True)
    dfagg = dfagg.set_index(datecol).pivot(columns='quantile', values=val).reset_index()
    dfagg[datecol] = pd.to_datetime(dfagg[datecol].astype('str'))
    return dfagg

def plot_one_group(fig, ax1, df,color='k', label=None):
    ax1.plot(df['deed_date'],df[0.5],color=color,label=label)
    ylo = df[0.25]
    yhi= df[0.75]
    ax1.fill_between(df['deed_date'],ylo ,yhi,alpha=0.1,color=color,label=None )
    return fig, ax1

#plot the aggregated data for burton joyce and compare to national average
plt.close()
fig = plt.figure()
ax1 = fig.add_subplot(111)
agg_bj = group_houseprice(dfbj,datecol='deed_date',val='price_paid',cadence='M')
fig, ax1 = plot_one_group(fig, ax1, agg_bj, color='b',label='Burton Joyce')

agg_all = group_houseprice(df,datecol='deed_date',val='price_paid',cadence='M')
fig, ax1 = plot_one_group(fig, ax1, agg_all, color='r',label='All Notts')

ax1.set_ylim([0,500000])
ax1.set_ylabel('£')
ax1.set_title('median house price\n3-month rolling average')
plt.legend()
plt.tight_layout()
plt.savefig('house_price_burtonjoyce.pdf')

datecol='deed_date'
cadence='M'
val = 'price_paid'
agg = df[[datecol,val]].groupby(datecol).quantile([0.25,0.5,0.75]).reset_index()
agg.columns=[datecol,'quantile',val]
agg = agg.set_index(datecol).pivot(columns='quantile',values=val).reset_index()
