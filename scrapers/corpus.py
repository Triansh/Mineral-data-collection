import os
import sys
from datetime import datetime
import logging

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
        self.save_csv_path = os.path.join(os.getcwd(), out_dir, f'minerals-{date_time}.csv')
        self.skip_path = os.path.join(os.getcwd(), out_dir, f'minerals-skipped-{date_time}.txt')
        log_file_path = os.path.join(os.getcwd(), log_dir, f'run-{date_time}.log')

        self.logger = get_logger(log_file_path)

        with open(input_path, 'r') as f:
            self.minerals = [x.rstrip() for x in f]

        self.df = pd.DataFrame()
        self.skipped_minerals = []

    def get_data(self):
        for idx, m in enumerate(self.minerals):
            self.search(m)
            if (idx + 1) % 100 == 0:
                self.load_data_in_files()
                self.logger.info(f"Total {idx + 1} (1-based) minerals processed and written.")

        self.load_data_in_files()
        self.logger.info('All processing done!!🥳🥳')

    def search(self, topic):
        page = wikipedia.search(topic)
        if len(page) <= 0:
            print('No results')
            return
        page = page[0]
        page_data = wptools.page(page).get_parse()
        if page_data.data['infobox'] is not None:
            infobox = {k.lower(): v for k, v in page_data.data['infobox'].items()}
            mineral_df = pd.DataFrame.from_records([infobox])
            self.df = self.df.append(mineral_df)
        else:
            self.skipped_minerals.append(topic)

    def load_data_in_files(self):
        self.df.to_csv(path_or_buf=self.save_csv_path)
        with open(self.skip_path, 'w') as f:
            f.write('\n'.join(self.skipped_minerals))


if __name__ == "__main__":
    input_file_path = sys.argv[1]
    log_directory = sys.argv[2]
    scraper = Scraper(input_file_path, './data/wikipedia', log_directory)
    scraper.get_data()
