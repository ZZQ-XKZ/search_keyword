#!/usr/bin/env python

import schedule
import time
from subprocess import call
import argparse

keyword = ""


def Search():
    global keyword
    print(keyword)
    call([
        "scrapy",
        "crawl",
        "search_baidu",
        "-s",
        "LOG_FILE="+keyword+".log",
        "-a", "keyword="+keyword,
        "-a", "page_count=10"
    ])

    call([
        "scrapy",
        "crawl",
        "search_google",
        "-s",
        "LOG_FILE="+keyword+".log",
        "-a", "keyword="+keyword,
        "-a", "page_count=10"
    ])

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyword')
    args = parser.parse_args()
    keyword = args.keyword
    schedule.every(1).minutes.do(Search)
    while True:
        schedule.run_pending()
        time.sleep(1)