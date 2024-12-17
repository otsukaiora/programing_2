import pandas as pd

orders = pd.read_csv('/Users/iora/lecture/PR2/orders.csv')
items = pd.read_csv('/Users/iora/lecture/PR2/items.csv')

merged = pd.merge(orders, items, on='item_id')

merged['purchase_amount'] = merged['item_price'] * merged['order_num']

average_user = merged.groupby('user_id')['purchase_amount'].mean().reset_index()

highest_user = average_user.loc[average_user['purchase_amount'].idxmax()]

print([highest_user['user_id'], highest_user['purchase_amount']])