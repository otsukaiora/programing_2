import pandas as pd

orders = pd.read_csv('/Users/iora/lecture/PR2/orders.csv')
items = pd.read_csv('/Users/iora/lecture/PR2/items.csv')

merged = pd.merge(orders, items, on='item_id')

merged['purchase_amount'] = merged['item_price'] * merged['order_num']

max_order = merged.loc[merged['purchase_amount'].idxmax()]

print([max_order['order_id'], max_order['purchase_amount']])