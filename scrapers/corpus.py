import json
import os
import re
import sys
from datetime import datetime
import logging
from pprint import pprint

import pandas as pd
import wikipedia
import wptools

"""
Args:
    sys.argv[1]: Input file path (Path to minerals.txt file)
    sys.argv[2]: Path of log directory (Path of data/wikipedia)
Result:
    1) Read data from input file given
    2) Data collection and scraping
    3) Output 2 files, one csv having data collected and other having a list of skipped data
    4) Log files will be present in logs folder
Note:
    If running from root of project, you can use this command
    python scrapers/corpus.py minerals.txt data/wikipedia logs/
"""


def get_logger(log_file_path):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


class Scraper(object):

    def __init__(self, in_path, out_dir, log_dir):

        input_path = os.path.join(os.getcwd(), in_path)
        date_time = datetime.now().strftime("%d-%m_%H:%M:%S")
        self.save_json_path = os.path.join(os.getcwd(), out_dir, f'minerals-{date_time}.json')
        self.skip_path = os.path.join(os.getcwd(), out_dir, f'minerals-skipped-{date_time}.txt')
        log_file_path = os.path.join(os.getcwd(), log_dir, f'run-{date_time}.log')

        self.logger = get_logger(log_file_path)

        with open(input_path, 'r') as f:
            self.minerals = [x.rstrip() for x in f][1761:]

        self.df = pd.DataFrame()
        self.skipped_minerals = []
        self.all_min_dict = {}
        self.min_dict = {}

    def get_data(self):
        for idx, m in enumerate(self.minerals):
            self.min_dict = {}
            self.search(m + ' mineral')
            self.load_data_in_files()
            self.logger.info(f"{idx + 1} minerals processed and written.")

        self.load_data_in_files()
        self.logger.info('All processing done!!🥳🥳')

    def search(self, topic):
        page = wikipedia.search(topic)
        if len(page) <= 0:
            print('No results')
            return
        page = wptools.page(page[0])
        page_data = page.get().data
        pprint(page_data)
        if 'infobox' in page_data and page_data['infobox'] is not None:
            infobox = {k.lower(): v for k, v in page_data['infobox'].items()}
            self.min_dict.update(infobox)
        if 'description' in page_data:
            self.min_dict['description'] = page_data['description']
        if 'wikidata' in page_data and page_data['wikidata'] is not None:
            wikidata = {k.lower(): v for k, v in page_data['wikidata'].items()}
            self.min_dict.update(wikidata)

        if len(self.min_dict) == 0:
            self.skipped_minerals.append(topic)
        elif 'label' in page_data:
            self.all_min_dict[page_data['label']] = self.min_dict
        else:
            self.all_min_dict[page_data['title']] = self.min_dict

    def load_data_in_files(self):
        with open(self.save_json_path, 'w') as f:
            json.dump(self.all_min_dict, f)
        with open(self.skip_path, 'w') as f:
            f.write('\n'.join(self.skipped_minerals))


if __name__ == "__main__":
    # input_file_path = sys.argv[1]
    # log_directory = sys.argv[2]
    scraper = Scraper('./mineral_list.txt', './data/wikipedia', './logs')
    scraper.get_data()
