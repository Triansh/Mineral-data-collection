import sys
import pandas as pd

from tabula import read_pdf


def get_data(input_path):
    """
    The function is responsible for extracting all the data covered
    in ruling lines and add it in a dataframe.

    :param input_path: The path to input pdf
    :return: Dataframe combining all data
    """
    if not input_path:
        input_path = "./data/ima/ima-mineral-list.pdf"

    dfs = read_pdf(input_path, lattice=True, pages='all',
                   pandas_options={'header': None})
    print(f"Found {len(dfs)} tables")

    column_names = ['name', 'formula', 'IMA status', 'IMA Year', 'Country', 'First ref',
                    'Second ref']
    main_df = pd.DataFrame(columns=column_names)
    rows = dfs[0].index[[0]]
    dfs[0].drop(rows, inplace=True)

    for df in dfs[:-1]:
        df.columns = column_names
        main_df = main_df.append(df)
    return main_df


def clean_df(df):
    """
    The function changes \r instances to ' '.
    If these \r instances are not removed, it causes issues in reading data when dumped.

    :param df: The input df to clean
    :return: The cleaned df
    """
    for c in df.columns:
        df[c] = df[c].apply(lambda x: x.replace('\r', ' ') if pd.notnull(x) else x)
    return df


if __name__ == "__main__":
    try:
        input_path = sys.argv[1]
    except:
        input_path = None
    df = get_data(input_path)
    clean_df(df)
    df.to_csv('./data/ima/ima-list.csv')
