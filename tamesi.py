

import pandas as pd

df = pd.read_csv('/Users/iora/lecture/PR2/winequality-red.csv')

print(df.head())

df[4:10]

slided_df = df[4:10]
styles = {
    'border': '1px solid black'
}

styled_slided_df = slided_df.style.set_table_styles([{
    'selector': 'th',
    'props': [('border', '1px solid black')]
}]).set_properties(**styles)
styled_slided_df

print( df[4:10] )