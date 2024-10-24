import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def create_group(data_save, h_gap):
    m_gap = h_gap * 60
    print(m_gap, "Minutes")
    le = LabelEncoder()
    data_save['mark'] = data_save.index
    data_save['mark'][(data_save['gap_time'] < m_gap)] = np.nan
    data_save['mark'] = data_save['mark'].fillna(method='bfill')
    data_save[f'group_id_hour_{h_gap}'] = le.fit_transform(data_save['mark'].astype(str))
    del data_save['mark']
    return data_save

# Load the data
data = pd.read_csv(r"dataset\eth_std_transactions.csv")
print('Data loaded successfully!', len(data))

# Drop duplicates
data = data.drop_duplicates()
print('Duplicates dropped successfully!', len(data))

# Filter only relevant columns and transactions with value > 0
data['value'] = pd.to_numeric(data['value'], errors='coerce')  # Convert value column to numeric
data = data[data['value'] > 0]
print('Relevant columns and transactions with value > 0 filtered successfully!', len(data))

# Convert timestamp to datetime
data['time'] = pd.to_datetime(data['timeStamp'], unit='s')

# Group by relevant columns
group_cols = ['to', 'value']
data_save = data.copy()

# Create group_id
data_save_desc = data_save.groupby(group_cols).agg({'from': 'nunique'})
data_save_desc = data_save_desc.rename(columns={'from': 'address_cnt'})
data_save_desc = data_save_desc.sort_values(by=['address_cnt'], ascending=False)
data_save_desc['group_id'] = list(range(len(data_save_desc)))
data_save_desc = data_save_desc.reset_index()

data_save = data_save.merge(data_save_desc, how='left', on=group_cols)

# Sort and calculate time differences
data_save = data_save.sort_values(by=['group_id', 'time'])
data_save['time1'] = data_save.groupby(['group_id']).time.transform(lambda x: x.shift(-1))
data_save['rank'] = data_save.groupby(['group_id']).time.transform(lambda x: x.rank(method='dense'))
data_save['gap_time'] = (data_save['time1'] - data_save['time']).dt.total_seconds() / 60

# Create time-based groups
hour_list = [0.5]
for h in hour_list:
    data_save = create_group(data_save, h)

hour_group = [f'group_id_hour_{h}' for h in hour_list]
hour_group += ['group_id']

# Calculate statistics for each group
for tg_group_id in hour_group:
    print(tg_group_id)
    data_save_desc2 = data_save.groupby([tg_group_id]).agg({'from': 'nunique'})
    data_save_desc2 = data_save_desc2.rename(columns={'from': f'address_cnt_{tg_group_id}'})
    data_save = data_save.merge(data_save_desc2, how='left', on=[tg_group_id])
    
    data_save = data_save.sort_values(by=[tg_group_id, 'time'])
    data_save[f'time_{tg_group_id}'] = data_save.groupby([tg_group_id]).time.transform(lambda x: x.shift(-1))
    data_save['rank'] = data_save.groupby([tg_group_id]).time.transform(lambda x: x.rank(method='dense'))
    data_save[f'gap_time_{tg_group_id}'] = (data_save[f'time_{tg_group_id}'] - data_save['time']).dt.total_seconds() / 60

# Define helper functions for time-based calculations
def get_time_per(gap_list_or, v):
    gap_list = [gap for gap in gap_list_or if gap >= 0]
    return np.percentile(gap_list, v) if len(gap_list) > 0 else np.nan

def get_time_std(gap_list_or):
    gap_list = [gap for gap in gap_list_or if gap >= 0]
    return np.std(gap_list) if len(gap_list) > 0 else np.nan

def get_time_mean(gap_list_or):
    gap_list = [gap for gap in gap_list_or if gap >= 0]
    return np.mean(gap_list) if len(gap_list) > 0 else np.nan

# Calculate time-based statistics for each group
for tg_group_id in hour_group:
    print(tg_group_id)
    data_save = data_save.sort_values(by=[tg_group_id, 'time'])
    
    for p in [1, 5, 10, 25, 50, 75]:
        data_save[f'time_{p:02d}_p_{tg_group_id}'] = data_save.groupby([tg_group_id])[f'gap_time_{tg_group_id}'].transform(lambda x: get_time_per(x, p))
    
    # Calculate time-based statistics
    data_save[f'time_std_{tg_group_id}'] = data_save.groupby([tg_group_id])[f'gap_time_{tg_group_id}'].transform(get_time_std)
    data_save[f'time_mean_{tg_group_id}'] = data_save.groupby([tg_group_id])[f'gap_time_{tg_group_id}'].transform(get_time_mean)
    data_save[f'time_cov_{tg_group_id}'] = data_save[f'time_std_{tg_group_id}'] / data_save[f'time_mean_{tg_group_id}']

# Save the results
data_save.to_csv(r"bulkDonation/getData.csv", index=False)