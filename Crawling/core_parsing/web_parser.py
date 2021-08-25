"""
대규모 크롤링(여러가지 검색 엔진 사이트(google naver bing daum)을 해서 (내가 진행하고있음)
"""
import re
import time
import logging
import threading
from collections import deque

import requests
import urllib3
from bs4 import BeautifulSoup
from requests import exceptions
from urllib.parse import urlparse
from Crawling.core_parsing import database
from Crawling.core_parsing.utility import GoogleSeleniumUtility

# 방문 큐 만들기 설계 진행해야함
# visit_site = deque()
# visited_site = deque()
# expected_site = deque()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# database
insert_base = database.MysqlConnect()


# html data paring
class UrlParsingDriver(GoogleSeleniumUtility):
    def __init__(self, data, count=5):
        super(UrlParsingDriver, self).__init__(data=data, count=count)
        self.ignore_tag = '#'
        self.ignore_url = re.compile('^(http|https)+://(webcache)')
        self.ignore_search = re.compile('^/(search)|(related:)')
        self.soup = None

    def search_data(self):
        if self.soup is None:
            return

        # a tag -> h3 tag location
        # GoogleSeleniumUtility 상속
        try:
            # google search div box <div id='rso>
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
                logging.info(f'link -> {get_link}, title -> {get_text},  status_code -> {status}')
                total_url = UrlCreate(object_url=get_link).url_addition()
                a = CounterTag().count_a_tag_url(total_url)
                # db insert
                # insert_base.url_status_db_insert(total_url, status, get_text, a[0])
                insert_base.url_tag_db_insert(total_url, a[0], a[1], a[2])

        except (exceptions.ConnectionError, exceptions.RequestException):
            raise TypeError

    def main_stream(self):
        soup = self.next_page_injection()
        for i in soup:
            self.soup = BeautifulSoup(i, 'lxml-xml')
            self.search_data()


# url create documentation
class UrlCreate:
    def __init__(self, object_url, url='https://google.com'):
        self.url = url
        self.object_url = object_url

    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}/'

    # /~ 로 끝나는 url 붙여주는 함수
    def url_addition(self):
        link = self.url_create() + self.object_url if self.object_url.startswith('/') else self.object_url
        return link


class CounterTag:
    def __init__(self):
        self.soup = None

    def count_a_tag_url(self, url):
        res = requests.get(url)
        soup = self.soup = BeautifulSoup(res.content, 'lxml-xml')
        a_count = [a_tag for a_tag in soup.find_all('a')]
        href = [a_tag['href'] for a_tag in soup.find_all('a')]
        text = [a_tag.h3 for a_tag in soup.find_all('a')]
        return len(a_count), len(href), len(text)
