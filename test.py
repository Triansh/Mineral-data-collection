import pandas as pd
import numpy as np

# if __name__ == "__main__":
# df = pd.read_csv('./data/athlete/athlete_15_10_2021_16_46_44.csv', index_col=0)
# df = df.drop(columns=['intro.value', 'name.xml:lang'])
# # print(df)
# df.columns = ['link', 'DOB', 'height', 'name', 'country', 'language']
# # df.fillna(0)
# # df = df.dropna()
# # print(df)
# df = df.drop_duplicates(subset=['link'], keep='last').reset_index(drop=True)
# df['link'] = df['link'].apply(lambda x: x.replace(' http://dbpedia.org/resource/', ''))
# # df = df.drop(columns=['link'])
# # df.to_csv(path_or_buf='data.csv', index=False)
# print(df)
# import re
#
# reg = re.compile(r"\*\[\[.*\]\]")
#
# t = []
# with open('./output.txt', 'r') as f:
#     for line in f:
#         if reg.match(line):
#             id = line.find(']]')
#             t.append(line[3:id])
#
# print(len(t))
# with open('./minerals.txt', 'w') as f:
#     f.write('\n'.join(t))


# df = pd.read_csv('./mineral_data.csv')
# print(df.info(verbose=True, max_cols=200))
# print((df['strunz'] != '').sum())
# for c in df.columns:
#     if df[]


