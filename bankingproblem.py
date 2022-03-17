# -------   The Banking Problem ---------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def banking_problem(filename, stock):
    df = pd.read_csv(filename, \
                          parse_dates={'DateTime': ['Date','Time']})

    # 1ο ερώτημα

    max_request = df['Value'].max()
    min_request = df['Value'].min()

    print('Max request = ', max_request)
    print('Min request = ', min_request)


  # 2ο ερώτημα

    max_deposit = df[df['Request'] == 'Deposit']['Value'].max()
    min_deposit =df[df['Request'] == 'Deposit']['Value'].min()

    max_withdrawal = df[df['Request'] == 'Withdrawal']['Value'].max()
    min_withdrawal = df[df['Request'] == 'Withdrawal']['Value'].min()

    print('Max deposit =', max_deposit)
    print('Min deposit = ', min_deposit)
    print('Max withdrawal = ', max_withdrawal)
    print('Min withdrawal = ', min_withdrawal)


    # 3ο ερώτημα

    total_requests = df.shape[0]
    deposit_requests = df[df['Request'] == 'Deposit'].shape[0]
    withdrawal_requests = df[df['Request'] == 'Withdrawal'].shape[0]

    print('Total requests = ', total_requests)
    print('Deposit requests = ', deposit_requests)
    print('Withdrawal requests = ', withdrawal_requests)


    plt.pie([deposit_requests, withdrawal_requests],\
     labels=['Deposit requests', 'Withdrawal requests'],\
           shadow= True, autopct= '%1.1f%%')

    plt.title('Deposits vs Withdrawals')
    plt.show()

    deposit_ratio = deposit_requests/total_requests
    withdrawal_ratio = withdrawal_requests/total_requests
    print(f'Deposit ratio = {100*deposit_ratio:.2f} %')
    print(f'Withdrawal ration = {100*withdrawal_ratio:.2f} %')

    # 4ο Ερώτημα

    s = df[df['Request'] == 'Withdrawal']['Value'].copy(deep = True)
    s[s<=300] *=0.99
    s[np.greater(s,300) & np.less_equal(s,500)] *= 0.98
    s[np.greater(s,500) & np.less_equal(s,1000)] *= 0.97
    s[np.greater(s,1000) & np.less_equal(s,1500)] *=0.95
    s[np.greater(s,1500) & np.less_equal(s,2000)] *=0.93
    s[s>2000] *=0.92

    max_with_after_tax = s.max()
    print(f'Max request for withdrawal after tax = {max_with_after_tax:.2f}')

    df.loc[df['Request'] == 'Withdrawal', 'Value'] = -s
    df.sort_values(by = ['DateTime', 'Value'], inplace= True,\
                   ignore_index= True)

    # 5o Ερώτημα

    current_stock = stock
    total_executed_requests =0
    bank_account = []
    for i in range(len(df)):
        if (current_stock + df['Value'][i] >=0):
            current_stock+= df['Value'][i]
            total_executed_requests+=1
            bank_account.append(current_stock)
        else: bank_account.append(current_stock)

    print('Total executed requests = ', total_executed_requests)
    print(f'Percentage of total executed requests \
{100*total_executed_requests/total_requests:.2f} %')

    # Ερώτημα 6

    df['Bank account'] = bank_account
    total_time = (df['DateTime'].max()-df['DateTime'].min()).seconds
    mean_value = 0
    for i in range(len(df)-1):
        mean_value += (df.iloc[i+1,0]-df.iloc[i,0]).seconds * df.iloc[i,3]

    print(f'Mean value = {mean_value/total_time:.3f}')

    # Ερώτημα 7

    fig, ax = plt.subplots(figsize = (10,10))
    xaxis = df['DateTime']
    weights = df['Bank account']

    plt.fill_between(df['DateTime'],df['Bank account'], alpha=0.7, step="pre")
    ax.step(xaxis, weights)
    plt.show()

    # Ερώτημα 8

    fig, ax = plt.subplots(figsize = (10,10))
    plt.fill_between(df['DateTime'],df['Value'].cumsum()+stock, alpha=0.7, step="pre")
    plt.step(df['DateTime'], df['Value'].cumsum()+stock, drawstyle = 'steps')
    #plt.savefig('Bank.png')
    plt.show()

    # Ερώτημα 9

    minimum_stock_required = abs(df['Value'].cumsum().min())
    print(f'Minimum required stock to fullfill all requests\
    = {minimum_stock_required:.2f}')

    # Histogram of the stock of the bank if initial stock = 78512 (ceil(minimum_stock))

    fig, ax = plt.subplots(figsize = (10,10))
    plt.fill_between(df['DateTime'],df['Value'].cumsum()+np.ceil(minimum_stock_required), alpha=0.7, step="pre")

    ax.step(df['DateTime'], df['Value'].cumsum()+np.ceil(minimum_stock_required))

    #ax.step(df['DateTime'], df['Value'].cumsum()+np.ceil(minimum_stock_required)) 
    # Is step looking better than the histogram?

    plt.show()

banking_problem(sys.argv[1],int(sys.argv[2])) # Be careful stock must be int

    
