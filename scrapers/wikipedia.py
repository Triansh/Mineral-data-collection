import json
import logging
import os
import sys
from datetime import datetime

import wikipedia
import wptools


def get_logger(log_file_path):
    """
    Setup for logger

    :param log_file_path: The file path where statements will be logged.
    :return: instance of logger
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


class Scraper(object):

    def __init__(self, in_path, out_dir='./data/wikipedia', log_dir='./logs'):
        """
        The class is responsible for searching the mineral, retrieving its data,
        storing the data into json, and dumping the json file in output directory.

        The function retrieves minerals from input file, initializes required dictionaries.
        We use current timestamp to name the output and log files.

        :param in_path: path of file containing a list of mineral separated by \n
        :param out_dir: path of output directory, defaults to data/wikipedia/
        :param log_dir: path of logs directory, defaults to logs/
        """

        input_path = os.path.join(os.getcwd(), in_path)
        date_time = datetime.now().strftime("%d-%m_%H:%M:%S")
        self.save_json_path = os.path.join(os.getcwd(), out_dir, f'minerals-{date_time}.json')
        self.skip_path = os.path.join(os.getcwd(), out_dir, f'minerals-skipped-{date_time}.txt')
        log_file_path = os.path.join(os.getcwd(), log_dir, f'run-{date_time}.log')

        self.logger = get_logger(log_file_path)

        with open(input_path, 'r') as f:
            self.minerals = [x.rstrip() for x in f][1761:]

        self.skipped_minerals = []
        self.all_min_dict = {}
        self.min_dict = {}

    def get_data(self):
        """
        The function shows a procedure which is repeated for each mineral
        to retrieve its data.

        :return: None
        """
        for idx, m in enumerate(self.minerals):
            self.min_dict = {}
            self.search(m + ' mineral')
            self.load_data_in_files()
            self.logger.info(f"{idx + 1} minerals processed and written.")

        self.load_data_in_files()
        self.logger.info('All processing done!!🥳🥳')

    def search(self, topic):
        """

        The function first searches the relevant regarding the topic in wikipedia. Once we
        obtain the page, we retrieve all its data from wikidata and wikipedia info boxes
         using wptools library.
         Once retrieved, update the dictionary that stores data of every mineral.
         If search failed and we didn't receive any data, the mineral name is pushed in
         a skipped minerals list.

        :param topic: Topic to search for (in our case, mineral name)
        :return:  None
        """
        page = wikipedia.search(topic)
        if len(page) <= 0:
            print('No results')
            return
        page = wptools.page(page[0])
        page_data = page.get().data
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
        """
        Dump the data obtained in the dictionary and the skipped list into output directory.

        :return: None
        """
        with open(self.save_json_path, 'w') as f:
            json.dump(self.all_min_dict, f)
        with open(self.skip_path, 'w') as f:
            f.write('\n'.join(self.skipped_minerals))


if __name__ == "__main__":
    input_file_path = sys.argv[1]
    scraper = Scraper(input_file_path, )
    scraper.get_data()
