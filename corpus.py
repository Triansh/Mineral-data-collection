import os
import sys

import wikipedia
import wptools
import pandas as pd


class Scraper(object):

    def __init__(self):
        with open(os.path.join(os.getcwd(), 'minerals.txt'), 'r') as f:
            self.minerals = [x.rstrip() for x in f]
        self.df = pd.DataFrame()
        self.skipped_minerals = []

    def get_data(self):
        for idx, m in enumerate(self.minerals):
            self.search(m)
            if (idx + 1) % 100 == 0:
                self.load_data_in_files()
                print(f"Total {idx + 1} (1-based) minerals processed and written.")
        self.load_data_in_files()

    def search(self, topic):
        page = wikipedia.search(topic)[0]
        page_data = wptools.page(page)
        page_data.get_parse()
        if page_data.data['infobox'] is not None:
            infobox = {k.lower(): v for k, v in page_data.data['infobox'].items()}
            mineral_df = pd.DataFrame.from_records([infobox])
            self.df = self.df.append(mineral_df)
        else:
            self.skipped_minerals.append(topic)

    def load_data_in_files(self):
        save_path_csv = os.path.join(os.getcwd(), 'data/wikipedia', 'minerals-1.csv')
        save_path_skipped = os.path.join(os.getcwd(), 'data/wikipedia', 'skipped.txt')
        self.df.to_csv(path_or_buf=save_path_csv)
        with open(save_path_skipped, 'w') as f:
            f.write('\n'.join(self.skipped_minerals))


if __name__ == "__main__":
    scraper = Scraper()
    scraper.get_data()
