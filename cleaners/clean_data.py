import os
import sys
import pandas as pd
import re

"""
Args:
    sys.argv[1]: Input file path (csv file to clean)
    sys.argv[3]: Path of output csv file (Path of data/wikipedia)
Note:
    If running from root of project, you can use this command
    python cleaners/clean_data.py data/wikipedia/mineral_data.csv minerals.txt data/wikipedia/clean-mineral-data.csv > out.txt 
"""

name_reg = re.compile(r"[^(\w| |\[|\]|\(|\)|-]+")
sys_cat_regex = re.compile(r"[\w\s,-]+")

rogue_words = {'hlist', 'flatlist', 'plainlist', 's', 'br', '',
               'overline', 'list'}


# remove_html = re.compile(r"<.*?/>|<[^>]>.*?</[^>]>")
# bracket_cleaner = re.compile(r"\[|\]")
#
#
# def clean(text):
#     text = remove_html.sub(text, ' ')
#     text = ''.join(bracket_cleaner.split(text))
#     text = ' '.join(text.split())
#     return text

def clean_sys_cat(pat: str):
    if pd.isnull(pat):
        return pat
    # print(pat)
    pat = pat.replace('|', ',')
    content = ''.join([' ' if x.strip() in rogue_words else x for x in sys_cat_regex.findall(pat)])
    return content


synonyms = [('color', 'colour'), ('luster', 'lustre')]

# Under process
if __name__ == "__main__":
    path_to_csv = os.path.join(os.getcwd(), sys.argv[1])
    df = pd.read_csv(path_to_csv)

    df = df.drop(columns=['image', 'caption', 'imagesize'], errors='ignore')
    df = df.dropna(subset=["name"]).reset_index(drop=True)

    # print(df.columns.tolist())
    # print('Columns:', len(df.columns))

    for (x, y) in synonyms:
        # print(df[[x, y]].info())

        a = df.index[df[x].notnull()].tolist()
        b = df.index[df[y].notnull()].tolist()
        inter = list(set(a).intersection(set(b)))
        df[x] = df[x].combine_first(df[y])
        df = df.drop(columns=[y])

        # print(f"Intersection of {x} and {y}:", len(inter))
        # print(df[[x, y]].iloc[inter])
        # print(df[[x]].info())

    # Accept the column if has data in >= col_remove_perc % of all rows
    col_remove_perc = 40.0
    min_count = int((col_remove_perc / 100) * df.shape[0] + 1)
    df.dropna(axis=1, how='any', thresh=min_count, inplace=True)

    # Accept the row if it has data in >= row_remove_perc % of all columns
    #     row_remove_perc = 60.0
    #     min_count = int((row_remove_perc / 100) * df.shape[1] + 1)
    #     df.dropna(axis=0, how='any', thresh=min_count, inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(df.info())

    # Attribute wise cleanup here
    df['name'] = df['name'].apply(lambda x: ''.join(name_reg.split(x)))
    df['system'] = df['system'].apply(lambda x: clean_sys_cat(x))
    df['category'] = df['category'].apply(lambda x: clean_sys_cat(x))
    #     df['category'] = df['category'].apply(lambda x: clean_sys_cat(x))

    df.to_csv('./data/wikipedia/mineral-clean-1.csv', index=False, sep='\t')

    # Playing around with the data here! 😅
#     with open(os.path.join(os.getcwd(), sys.argv[2]), 'r') as f:
#         minerals = set([x.rstrip() for x in f])

#     for key in df.columns:
#         print(key, ": ")
#         print(df[key].iloc[:10])
#         print()
# df2 = df['name']
# print(df2)
# processed = set(df2.tolist())
# # clp  = processed.
# x = minerals.difference(processed)
# y = processed.difference(minerals)
# z = x.union(y)
# print('\n\n', len(x))
# print('\n'.join(sorted(z)))

# df.to_csv(path_or_buf=os.path.join(os.getcwd(), sys.argv[3]))

# print(df.isnull().sum().sum())
# print(df.isin([' ','NULL',0]).sum())

# for col in df.columns:
#     if (df[col]!='').sum() > 300:
#         print(col)
# df = df.loc[:, df.isin([' ', '','NULL',0]).sum() > 0]

# x = df.index[df['color'].notnull()].tolist()
# y = df.index[df['colour'].notnull()].tolist()
# # print(x, y)
# print((set(x).intersection(set(y))))
# print(df[['name', 'color', 'colour']].iloc[734])

# print(df.info(max_cols=200))
# df['color'] = df['color'].combine_first(df['colour'])
# df = df.drop(columns=['colour'])
# print(df.info(max_cols=200))
