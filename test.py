import pandas as pd
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

# reg = re.compile(r"\[\[.*?\]\]")

# with open('./out.txt', 'r') as f:
#     raw = reg.findall(''.join(f.readlines()))
#     raw = list(map(lambda x: x[2:-2], raw))

# with open('./minerals_extra.txt', 'w') as f:
#     f.write('\n'.join(raw))

df = pd.read_csv('./mineral_data.csv')
# print(df.isnull().sum().sum())
# print(df.isin([' ','NULL',0]).sum())
perc = 40.0
min_count =  int(((perc)/100)*df.shape[0] + 1)
df.dropna(axis=1, how='any', thresh=min_count, inplace=True)
df.head()
# for col in df.columns:
#     if (df[col]!='').sum() > 300:
#         print(col)
# df = df.loc[:, df.isin([' ', '','NULL',0]).sum() > 0]
print(df.info(verbose=True, max_cols=200))
