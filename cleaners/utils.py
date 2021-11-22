import json
from copy import deepcopy

import numpy as np
import pandas as pd
import unidecode
from nltk.corpus import wordnet


def get_synonyms(word):
    """
    Collects all the synonyms present for the word in nltk corpus and returns them

    :param word: The word whose synonyms are required
    :return:  A set of synonyms for the word
    """
    syns = [lm.name() for syn in wordnet.synsets(word) for lm in syn.lemmas()]
    return set(syns)


def remove_synonyms(df):
    """
    The function finds out all the synonyms of each column, if any of the synonym
    is present for a column, it merges both the columns and drops the synonym column.

    :param df: A dataframe whose synonym columns need to be merged
    :return: The processed dataframe
    """
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
    """
    Each entry in column col of dataframe df is made lowercase.

    :param df:  Dataframe
    :param col: column of dataframe
    :return:  dataframe with lowercase column
    """
    df[col] = df[col].apply(lambda x: x.lower())
    return df


def process_df(df):
    """
    Dataframe columns are sorted based on their names.
    mineral_name in the dataframe is marked as index column.
    All minerals within mineral_name attribute are also sorted.
    Mineral names are converted into lowercase letters and any accents are also removed.
    mineral_name column is moved in front of dataframe.

    :param df: Dataframe to process
    :return:  Processed dataframe
    """
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
    """
    Convert a json file into a dataframe.
    Format of json file
    {
        <mineral_name_1> : {
                <attr1_name> : <attr1_value>,
                <attr2_name> : <attr2_value>,
                ...
        },
        <mineral_name_2> : {...},
        ...
    }

    :param file_path: Path to json file
    :return: Dataframe
    """
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
    Used to filter out columns and rows from a dataframe by a threshold.

    :param df: Dataframe to be filtered
    :param axis:  axis = 0 for columns, axis = 1 for rows
    :param threshold: percentage threshold, defaults to 30%
    :return: Filtered dataframe
    """
    min_count = int((threshold / 100) * df.shape[axis] + 1)
    filtered_df = df.dropna(axis=int(not axis), how='any', thresh=min_count).reset_index(drop=True)
    return filtered_df


def get_all_cols(dfs):
    """
    Combines all the column names of dataframe into a set.
    :param dfs: List of dataframes
    :return: Set of column names
    """
    cols = set()
    for df in dfs:
        cols.update(df.columns)
    return cols


def get_column_diff(df1, df2, col1, col2=None):
    """
    This function is returns the set difference of entries present in col1 of dataframe 1 and
    col2 of dataframe 2.
    If col2 is absent, col2 is assigned same as col1.

    :param df1: Dataframe 1
    :param df2: Dataframe 2
    :param col1: Column of Dataframe 1
    :param col2: Column of Dataframe 2
    :return: Two set differences from either side
    """
    if col2 is None:
        col2 = col1
    set_1 = set(df1[col1].tolist()).difference(set(df2[col2].tolist()))
    set_2 = set(df2[col2].tolist()).difference(set(df1[col1].tolist()))
    return set_1, set_2


def strip_data(df):
    """
    Each entry in the dataframe is converted to string and any entry with 'nan' as string is
    modified to np.nan

    :param df: dataframe to strip
    :return: stripped data frame
    """
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().apply(lambda x: np.nan if x == 'nan' else x)
    return df
