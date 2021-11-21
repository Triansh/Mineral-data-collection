# IRE Major Project

## Overview

## Installation

* Ensure that you have python 3.8+ installed in your system.
* Clone/ Download the repository
* Run the following commands to create and activate a python environment in the root folder.

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Directory Structure

#### Crawlers

The directory contains only a single file which we used to obtain the links of various minerals in
Wikipedia. Further descriptions of the code can be found in the later sections.

#### Scrapers

The directory contains all the code used to scrape various data sources listed above. Each file is
responsible for scraping a single data source.

#### Data

A data folder is a place where all the scraped, processed and merged data is stored. It is further
divided into sub-directories to store data associated with each source.

#### Cleaners

This directory is responsible for merging and cleaning data obtained from the sources. The code is
divided into multiple files based on the use cases. It also contains a utils file that contains some
helper functions used in the cleaning and merging process.

##### Plots

This folder contains notebooks used to analyze data and create plots about data distribution.
Primary libraries used to create plots are matplotlib, seaborn and plotly.

#### Logs

This is a sample directory that is used to save logs obtained when scraping data from Wikipedia. The
scraping took a large time to finish, hence logging the output. A sample log is present in the
directory.

## How to run

Jupyter notebooks can be run cell by cell to obtain the output. 

The below section describes how to
explicitly run `.py` files used in scraping.

### Wikipedia scraping

Run the following commands to avoid any errors in the project root.

```shell
$ mkdir -p logs
$ mkdir -p data/wikipedia
$ python scrapers/wikipedia.py <input_file_path>
```

The output will be present in `data/wikipedia` directory. The corresponding log will be present
in`logs` directory.

### PDF scraping

**Ensure that you have Java 8+ installed in your system. The library `tabula-py` requires java
runtime environment.**

```shell
$ mkdir -p data/ima
$ python scrapers/ima_pdf.py <input_file_path>
```

The output will be present in `data/ima` directory. 

