import pandas as pd

items = pd.read_csv('/Users/iora/lecture/PR2/items.csv')

target_item_id = 101

target_item = items[items['item_id'] == target_item_id].iloc[0]
target_small_category = target_item['small_category']
target_big_category = target_item['big_category']
target_price = target_item['item_price']
target_pages = target_item['pages']

candidate_items = items[items['item_id'] != target_item_id]

candidate_items['category_score'] = (
    (candidate_items['small_category'] != target_small_category) +
    (candidate_items['big_category'] != target_big_category)
)

candidate_items['price_score'] = abs(candidate_items['item_price'] - target_price)

candidate_items['page_score'] = abs(candidate_items['pages'] - target_pages)

candidate_items['total_score'] = (
    candidate_items['category_score'] * 1000000 +
    candidate_items['price_score'] * 1000 +
    candidate_items['page_score']
)

recommended_ids = candidate_items.sort_values(by='total_score')['item_id'].head(3).tolist()

print([recommended_ids[0], recommended_ids[1], recommended_ids[2]])