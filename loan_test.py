import pandas as pd


def dataset(x, missing = ""):
    return pd.read_csv('Dataset/' + x + '.csv', sep = ';', low_memory = False, na_values = missing_values).rename(str.strip, axis = 'columns')

missing_values = ['?']
account_data = dataset('account', missing_values)
client_data = dataset('client', missing_values)
disp_data = dataset('disp', missing_values)
district_data = dataset('district', missing_values)
card_train = dataset('card_train', missing_values)
card_test = dataset('card_test')
loan_train = dataset('loan_train', missing_values)
loan_test = dataset('loan_test')
trans_train = dataset('trans_train', missing_values)
trans_test = dataset('trans_test')


# Normalize dates in client and create a new collumn to distinguish sex
new_col = []
i = 0
for line in client_data['birth_number']:
    if int(str(line)[2]) >= 5:
        client_data['birth_number'][i] = client_data['birth_number'][i] - 5000
        new_col.append('F')
    else:
        new_col.append('M')
    i+=1
        
client_data['Genre'] = new_col


# Build train dataset
train_data = loan_train
train_data = pd.merge(train_data, account_data, left_on='account_id', right_on='account_id', suffixes=('_loan', '_account'))

# only owner can issue permanent orders and ask for a loan
disp_owners = disp_data[disp_data.type.eq('OWNER')]
train_data = pd.merge(train_data, disp_owners, left_on = 'account_id', right_on = 'account_id', suffixes = ('', '_disp'))

train_data = pd.merge(train_data, district_data.set_index('code'), left_on = 'district_id', right_index = True)





district_data.merge(client_data, left_on='code',right_on='district_id')
