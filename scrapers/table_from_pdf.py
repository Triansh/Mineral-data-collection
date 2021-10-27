import pandas as pd
from tabula import read_pdf

dfs = read_pdf('./data/ima-mineral-list.pdf', lattice=True, pages='all',
               pandas_options={'header': None})
print(f"Found {len(dfs)} tables")

column_names = ['name', 'formula', 'IMA status', 'IMA Year', 'Country', 'First ref', 'Second ref']
main_df = pd.DataFrame(columns=column_names)
rows = dfs[0].index[[0]]
dfs[0].drop(rows, inplace=True)

for df in dfs[:-1]:
    print(df)
    df.columns = column_names
    main_df = main_df.append(df)

for c in main_df.columns:
    main_df[c] = main_df[c].apply(lambda x: x.replace('\r', ' ') if pd.notnull(x) else x)

print(main_df.info())
main_df.to_csv('./data/ima-list.csv')

# df = pd.read_csv('./data/ima-list.csv')
# print(df.info())
