"""
대규모 크롤링(여러가지 검색 엔진 사이트(google naver bing daum)을 해서 (내가 진행하고있음)
"""
import http
import re
import time
import logging
import multiprocessing
from collections import deque

import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from Crawling.core_parsing import database

# 방문 큐 만들기 설계 진행해야함
# visit_site = deque()
# visited_site = deque()
# expected_site = deque()

request_except = requests.exceptions
url_except = urllib3.exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# database
# insert_base = database.MysqlConnect()

"""
thread
  ▲
UrlParsing
  ▲
Sele
"""


# html data paring
class UrlParsingDriver:
    def __init__(self, url=None):
        self.ignore_tag = '#'
        self.ignore_url = re.compile('^(http|https)+://(webcache)')
        self.ignore_search = re.compile('^/(search)|(related:)')
        self.url = url
        self.soup = None

    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}/'

    # /~ 로 끝나는 url 붙여주는 함수
    def url_addition(self, url):
        link = self.url_create() + url if url.startswith('/') else url
        return link

    def search_data(self):
        if self.soup is None:
            return
        # a tag -> h3 tag location
        # GoogleSeleniumUtility 상속
        try:
            # google search div box <div id='rso'>
            for a_tag in self.soup.find('div', id='rso').find_all('a'):
                # href data 수집
                get_link = a_tag['href']
                get_text = a_tag.text

                if self.ignore_url.findall(get_link) or self.ignore_search.findall(get_link):
                    continue
                if self.ignore_tag == get_link:
                    continue

                # web page status code 200 ~ 405
                status = requests.get(get_link, verify=False).status_code
                time.sleep(1)

                # log
                logging.info(f'link -> {get_link}, title -> {get_text},  status_code -> {status}')

                # total_url = self.url_addition(get_link)
                # a = CounterTag().count_tag_url(total_url)

                # db insert
                # insert_base.url_tag_db_insert(total_url, get_text, a[0], a[1], a[2], a[3], a[4])
                # insert_base.url_status_db_insert(total_url, status, get_text, a[0], a[2])

        except (request_except.ConnectionError, url_except.MaxRetryError, url_except.ProtocolError,
                url_except.NewConnectionError):
            print('Error or schemaMissing')

    def count_tag_url(self):
        a_count = [a_tag for a_tag in self.soup.find_all('a')]
        a_href = [0 if a_tag == KeyError else a_tag.href for a_tag in self.soup.find_all('a')]
        link_count = [a_tag for a_tag in self.soup.find_all('link')]
        link_href = [0 if a_tag == KeyError else a_tag.href for a_tag in self.soup.find_all('link')]
        text = [a_tag.h3 for a_tag in self.soup.find_all('a')]

        return len(a_count), len(a_href), len(link_count), len(link_href), len(text)


if "__main__" == __name__:
    parser = UrlParsingDriver()

    p1 = multiprocessing.Process(target=parser.search_data, args=())
    p1.start()

    p2 = multiprocessing.Process(target=parser.url_create, args=())
    p2.start()

    p3 = multiprocessing.Process(target=parser.count_tag_url, args=())
    p3.start()

    p1.join()
    p2.join()
    p3.join()