import numpy as np
import pandas as pd
import matplotlib.pylab as plt





#df = pd.read_csv('./data/burton_joyce_data.csv')
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
    dfagg = df[[datecol, val]].groupby(datecol).agg(['median', 'std']).fillna(0).reset_index()
    dfagg.columns = [' '.join(col).strip() for col in dfagg.columns.values]
    dfagg.sort_values(by=datecol, inplace=True)
    dfagg[datecol]=pd.to_datetime(dfagg[datecol].astype('str'))
    dfagg[val+' median'] = dfagg[val+' median'].rolling(runningavg)
    #dfagg[datecol]=pd.to_datetime(dfagg[datecol].values)
    return dfagg



#plot the aggregated data for burton joyce and compare to national average
plt.close()
fig = plt.figure()
ax1 = fig.add_subplot(111)
agg_bj = group_houseprice(dfbj,datecol='deed_date',val='price_paid',cadence='M')
ax1.plot(agg_bj['deed_date'],agg_bj['price_paid median'],label='burton joyce')
#,agg_bj['price_paid std']
agg_all = group_houseprice(df,datecol='deed_date',val='price_paid',cadence='M')
ax1.plot(agg_all['deed_date'],agg_all['price_paid median'],label='all')
#,agg_all['price_paid std']
ax1.set_ylim([0,500000])
ax1.set_ylabel('median house price')
plt.legend()
plt.savefig('house_price_burtonjoyce.pdf')

