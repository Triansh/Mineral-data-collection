# # -*- coding: utf-8 -*-
# """
# Created on Wed Jan 16 23:03:34 2019
# @author: NRoy
# """
#
# import os
# import sys
# import argparse
# from datetime import datetime
# import pandas as pd
# from pandas import json_normalize
# from SPARQLWrapper import SPARQLWrapper, JSON
# from pandas import ExcelWriter
# import q_athletes
#
#
# class Helper:
#     @staticmethod
#     def generate_file_name(file_name):
#         """ Generates a file name to store the results"""
#         return file_name + '_' + str(datetime.now().strftime("%d_%m_%Y")) + '_' + str(
#             datetime.now().strftime("%H_%M_%S"))
#
#     @staticmethod
#     def write_to_excel(df, file_name):
#         """ Writes the results to an excel sheet """
#         formatted_file_name = Helper.generate_file_name(file_name)
#         writer = ExcelWriter(Config.DATA_FOLDER_PATH + '/' + formatted_file_name + '.xlsx')
#         df.to_excel(writer)
#         writer.save()
#         print('Done.')
#
#     @staticmethod
#     def write_to_csv(df, file_name):
#         """ Writes the results to a pickle file"""
#         formatted_file_name = Helper.generate_file_name(file_name)
#         df.to_csv(Config.DATA_FOLDER_PATH + '/' + formatted_file_name + '.csv')
#         print("-------------WRITING TO CSV COMPLETED-------------")
#
#     @staticmethod
#     def read_from_pickle(file_name):
#         """ Reads from a pickle file"""
#         df = pd.read_pickle(file_name)
#         print("-------------READ FROM PICKLE COMPLETED-------------")
#         return df
#
#     @staticmethod
#     def remove_type_columns(df):
#         """ Removes all data type columns"""
#         cols_to_remove = []
#         for column in df.columns:
#             if "type" in column:
#                 cols_to_remove.append(column)
#         df_cleaned = df.drop(columns=cols_to_remove)
#         return df_cleaned
#
#     @staticmethod
#     def create_data_folder(path):
#         """ To create a new folder to store query results """
#         try:
#             if not os.path.isdir(path):
#                 os.mkdir(path)
#         except Exception as e:
#             print(e)
#             print("Could not create folder at {}. Working Directory: {}".format(path,
#                                                                                 str(os.getcwd())))
#
#
# class Config:
#     DBPEDIA_URL = "http://dbpedia.org/sparql"
#     DBPEDIA_LIMIT = 10000
#     df = None
#     DATA_FOLDER_PATH = "Data"
#     ITERATIONS = 5
#
#
# def clean_data_and_save(df, fname):
#     """
#     For basic cleaning and saving the dataset.
#
#     :param df: Pandas DataFrame object
#     :param fname: Pickle File Name to store contents of df
#     :return: None
#     """
#     df = Helper.remove_type_columns(df)
#     Helper.write_to_csv(df, fname)
#
#
# def get_paginated_data(limit, offset, query, sparql, df):
#     """
#     To get paginated data using the query and enforcing limits since
#     DBpedia does not allow more that 10000 (CommonConfig.DBPEDIA_LIMIT) results
#
#     :param limit: number of query results to retrieve
#     :param offset: starting point of query results
#     :param query: the query
#     :param sparql: SPARQL Endpoint
#     :param df: DataFrame to append every scrape (iterative)
#     :return: DataFrame of <= 10000 results
#     """
#     print("Current limit value: " + str(limit))
#     print("Current offset value: " + str(offset))
#     formatted_query = query.get_query(limit, offset)
#     sparql.setQuery(formatted_query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     results = json_normalize(results['results']['bindings'])
#     df = df.append(results)
#     return df
#
#
# def scrape_dbpedia(query, sparql):
#     """
#     To scrape dbpedia iteratively since DBpedia does not allow more that 10000 results
#     :param query: the query from queries/<your query file>
#     :param sparql: sparql endpoint
#     :return: completed DataFrame
#     """
#     print("------Begin Scraping DBpedia-------")
#     print(datetime.now())
#
#     df = pd.DataFrame()
#     try:
#         for i in range(Config.ITERATIONS):
#             if i == 0:
#                 df = get_paginated_data(Config.DBPEDIA_LIMIT, i, query, sparql, df)
#             else:
#                 print("Length of data frame now :" + str(len(df)))
#                 prev_len = len(df)
#                 df = get_paginated_data(Config.DBPEDIA_LIMIT, len(df) + 1, query, sparql, df)
#                 if prev_len == len(df):
#                     break
#     except Exception as e:
#         print(e)
#         print("Error in scraping DBpedia. Revise configurations.")
#         if len(df) == 0:
#             print("No response collected. Exit.")
#             sys.exit(1)
#         else:
#             print("Collected rows: {}".format(len(df)))
#             print("Incomplete data is being downloaded.")
#     return df
#
#
# class Scraper(object):
#
#     def __init__(self):
#         self.sparql = SPARQLWrapper(Config.DBPEDIA_URL)
#
#
# if __name__ == "__main__":
#     # Inputs
#
#     # Initialize SPARQLWrapper
#     sparql = SPARQLWrapper(Config.DBPEDIA_URL)
#     query = None
#     print(sys.argv)
#     path_to_save_data = os.path.join(os.getcwd(), sys.argv[1])
#     Config.DATA_FOLDER_PATH = path_to_save_data
#     # Set Query based on input
#     df = scrape_dbpedia(q_athletes, sparql)
#
#     clean_data_and_save(df, "athlete")
#     print("Finished scraping DBpedia at: {}".format(datetime.now()))
