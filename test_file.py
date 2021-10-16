import sys
import wikipedia
import argparse
import os
import datetime
from bs4 import BeautifulSoup
from mediawikiapi import MediaWikiAPI
import logging
import wptools
import re

reg = re.compile('[[.?*]]')

def search(topic):
    page = wikipedia.search(topic)
    print(page)
    # page_data = wptools.page(page)
    # page_data.get()
    # print(page_data.data['wikitext'])

if __name__ == "__main__":
    search(sys.argv[1])