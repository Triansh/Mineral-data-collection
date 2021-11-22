import json
from copy import deepcopy

import numpy as np
import pandas as pd
import unidecode
from nltk.corpus import wordnet


def get_synonyms(word):
    syns = [lm.name() for syn in wordnet.synsets(word) for lm in syn.lemmas()]
    return set(syns)


def remove_synonyms(df):
    done_with = set()
    for col in df.columns:
        for syn in get_synonyms(col):
            if syn != col and syn in df.columns and syn not in done_with:
                print(f"{col} has synonym {syn}")
                df[col] = df[col].combine_first(df[syn])
                df = df.drop(columns=[syn])
                done_with.update([syn, col])
    return df


def to_lower(df, col):
    df[col] = df[col].apply(lambda x: x.lower())
    return df


def process_df(df):
    df.columns = [x.lower() for x in df.columns]
    df.sort_index(axis=1, inplace=True)
    df.sort_values('mineral_name', inplace=True)
    df = to_lower(df, 'mineral_name')
    df['mineral_name'] = df['mineral_name'].apply(lambda x: unidecode.unidecode(x))
    mid = df['mineral_name']
    df.drop(labels=['mineral_name'], axis=1, inplace=True)
    df.insert(0, 'mineral_name', mid)
    return df


def json_to_df(file_path):
    with open(file_path, 'r') as f:
        obj = json.load(f)
    records = []
    for k, v in obj.items():
        temp = deepcopy(v)
        temp['mineral_name'] = ''.join(k.split())
        records.append(temp)
    df = pd.DataFrame.from_records(records)
    df = process_df(df)
    return df


def filter_df(df, axis, threshold=30):
    """
    use axis = 0 to remove columns
    use axis = 1 to remove rows
    """
    min_count = int((threshold / 100) * df.shape[axis] + 1)
    filtered_df = df.dropna(axis=int(not axis), how='any', thresh=min_count).reset_index(drop=True)
    return filtered_df


def get_all_cols(dfs):
    cols = set()
    for df in dfs:
        cols.update(df.columns)
    return cols


def get_column_diff(df1, df2, col1, col2=None):
    if col2 is None:
        col2 = col1
    set_1 = set(df1[col1].tolist()).difference(set(df2[col2].tolist()))
    set_2 = set(df2[col2].tolist()).difference(set(df1[col1].tolist()))
    return set_1, set_2


def strip_data(df):
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().apply(lambda x: np.nan if x == 'nan' else x)
    return df
