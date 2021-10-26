import os
import json
import pandas as pd
from pprint import pprint

# s = set()
# with open('./minerals.txt', 'r') as f:
#     s.update([x.strip().lower() for x in f if x.strip() != ''])
#
# for file in os.listdir('./data/wikipedia/'):
#     if file.startswith('wiki_'):
#         with open(os.path.join('./data/wikipedia', file), 'r') as f:
#             for line in f:
#                 sp = line.split('|')
#                 s.add(sp[0].lower().strip())
#
# print(len(s))
# print()
# pprint(sorted(s))




data = {}
with open('./data/webmineral/FullMineralData113.json', 'r') as f:
    data = json.load(f)

new_data = []

for k, v in data.items():
    new_dic = v
    new_dic['Mineral name'] = k
    new_data.append(new_dic)


df = pd.DataFrame.from_records(new_data)

# Accept the column if has data in >= col_remove_perc % of all rows
col_remove_perc = 30.0
min_count = int((col_remove_perc / 100) * df.shape[0] + 1)
df.dropna(axis=1, how='any', thresh=min_count, inplace=True)

# Accept the row if it has data in >= row_remove_perc % of all columns
# row_remove_perc = 50.0
# min_count = int((row_remove_perc / 100) * df.shape[1] + 1)
# df.dropna(axis=0, how='any', thresh=min_count, inplace=True)

print(df.info())


df.to_csv('./data/webmineral/mineral-113.csv')