import pandas as pd
from datetime import datetime,timedelta
TIMEOUT = 60
today_date = datetime.now()
one_day_ago = today_date - timedelta(days=1)
two_day_ago = today_date - timedelta(days=2)
DATE = one_day_ago.strftime("%d%m%Y")
file_path = f"C:\\Users\\niraj.sharma\\QuickFox\\Pos_settlement\\download_path\\CPD_Issuing_SBL 14_{DATE}.xlsx"
actual_transactions = ['5TCN05','5TCN07']
reversal_transactions = ['5TCN06','5TCN25','5TCN27']

df = pd.read_excel(file_path,dtype=str)
filtered_df = df[(df['CARD_NUMBER'].str.startswith(('443832', '463726')))]
filtered_df1 = filtered_df[(filtered_df['TXN_CURR'].str.startswith('356'))]
actual_txn_df = filtered_df[filtered_df['TC'].isin(actual_transactions)].copy()
reversal_txn_df = filtered_df[~filtered_df['TC'].isin(actual_transactions)].copy()

print(len(actual_txn_df))

for index, row_actual in actual_txn_df.iterrows():
    for index_rev, row_reversal in reversal_txn_df.iterrows():
        if row_actual['AUTH_ID'] == row_reversal['AUTH_ID']:
            if row_actual['TXN_AMT'] == row_reversal['TXN_AMT']:
                # Remove from actual_txn_df
                actual_txn_df.drop(index, inplace=True)
                break
            
# actual_txn_df["Amount"] = float(str(actual_txn_df["TXN_AMT"]))*0.0015
# values = list(filtered_df_debit['MSC Fee'])
# sid_debit_misc = sum(float(value.replace(',', '')) if value is not None and ',' in str(value) else 0 if value is None else float(value) for value in values)
# sid_debit_misc =  '{:.2f}'.format(sid_debit_misc)

# The line `# sum(float(actual_txn_df['TXN_AMT'].tolist()))` is attempting to calculate the sum of the
# transaction amounts in the 'TXN_AMT' column of the `actual_txn_df` DataFrame after converting them
# to float values.\
    
# sum(float(actual_txn_df['TXN_AMT'].tolist()))

total_amt = sum(float(i) * 0.0015 for i in actual_txn_df['TXN_AMT'].tolist())
print(round(total_amt,2))