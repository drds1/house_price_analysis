import numpy as np
import pandas as pd
import matplotlib.pylab as plt

'''
util functions for house price analysis
'''
def get_data(file):
    df = pd.read_csv(file)
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
    df['deed_date'] = pd.to_datetime(df['deed_date'])
    return df[cols]

#groupby sale date monthly cadence
def group_houseprice(df,datecol='deed_date',val='price_paid',cadence='M',runningavg=3):
    df[datecol] = df[datecol].dt.to_period(cadence)
    dfagg = df[[datecol, val]].groupby(datecol).quantile([0.25, 0.5, 0.75]).reset_index()
    dfagg.columns = [datecol, 'quantile', val]
    dfagg.sort_values(by=datecol, inplace=True)
    dfagg = dfagg.set_index(datecol).pivot(columns='quantile', values=val).reset_index()
    dfagg[datecol] = pd.to_datetime(dfagg[datecol].astype('str'))
    return dfagg

def plot_one_group(fig, ax1, dfin,color='k', label=None):
    df = dfin.sort_values(by='deed_date')
    df = df.iloc[:-1,:]
    ax1.plot(df['deed_date'],df[0.5],color=color,label=label)
    ylo = df[0.25]
    yhi= df[0.75]
    ax1.fill_between(df['deed_date'],ylo ,yhi,alpha=0.1,color=color,label=None )
    return fig, ax1


'''
script to ingest, group data and generate plots
'''
if __name__ == '__main__':
    # data ingestion Data from hm land registry
    # https://landregistry.data.gov.uk/
    df = get_data('./data/all_notts.csv')
    # isolate burton joyce
    dfbj = df[df['locality'] == 'BURTON JOYCE']
    #load devon
    dfd = get_data('./data/all_devon.csv')
    # isolate exeter
    dfdex = dfd[dfd['district']=='EXETER']
    #load london
    #dfl = get_data('./data/all_london.csv')

    #group inputs together and indicate plotting colour
    data_dict = {'All Notts':[df,'b'],
                 'Burton Joyce':[dfbj,'r'],
                 'All Devon':[dfd,'g'],
                 'Exeter':[dfdex,'y']}

    #plot the aggregated data for burton joyce and compare to national average
    plt.close()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for label, data_info in data_dict.items():
        data, color = data_info
        agg = group_houseprice(data,datecol='deed_date',val='price_paid',cadence='M')
        fig, ax1 = plot_one_group(fig, ax1, agg, color=color,label=label)
    ax1.set_ylim([0,500000])
    ax1.set_ylabel('£')
    ax1.set_title('median house price\n3-month rolling average')
    plt.legend()
    plt.tight_layout()
    plt.grid(b=None, which='major', axis='both')
    plt.savefig('house_price_burtonjoyce.png')

