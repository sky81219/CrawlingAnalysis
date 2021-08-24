"""
대규모 크롤링(여러가지 검색 엔진 사이트(google naver bing daum)을 해서 (내가 진행하고있음)
"""
import re
import logging
import threading
import time
from collections import deque

import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests import exceptions
from Crawling.core_parsing.utility import GoogleSeleniumUtility
from Crawling.core_parsing.utility import click_url

visit_site = deque()
visited_site = deque()
expected_site = deque()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# url create documentation
class UrlCreate(threading.Thread):
    def __init__(self, url='https://google.com'):
        threading.Thread.__init__(self)
        self.url = url

    # threading 할당
    def run(self):
        UrlCreate()

    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}/'

    # /~ 로 끝나는 url 붙여주는 함수
    def url_addition(self, url):
        link = self.url_create() + url if url.startswith('/') else url
        return link


# url create 객체 선언
create_url = UrlCreate()


# html data paring
link_s = []
class UrlParsingDriver(GoogleSeleniumUtility):
    def __init__(self, data, count=5):
        super(UrlParsingDriver, self).__init__(data=data, count=count)
        self.ignore_tag = '#'
        self.ignore_url = re.compile('^(http|https)+://(webcache)')
        self.ignore_search = re.compile('^/(search)|(related:)')
        self.soup = None

    def search_data(self):
        global link_s
        if self.soup is None:
            return

        # a tag -> h3 tag location
        # GoogleSeleniumUtility 상속

        try:
            # google search div box <div id='rso>
            for a_tag in self.soup.find('div', id='rso').find_all('a'):
                time.sleep(1)
                get_link = a_tag['href']

                get_text = a_tag.text
                if self.ignore_url.findall(get_link) or self.ignore_search.findall(get_link):
                    continue
                if self.ignore_tag == get_link:
                    continue
                # web page status code 200 ~ 405
                req = requests.get(get_link, verify=False).status_code
                logging.info(f'link -> {get_link}, title -> {get_text},  status_code -> {req}')
                link_s.append(get_link)

                return link_s
        except (exceptions.ConnectionError, exceptions.RequestException):
            raise TypeError

    def get_url(self):
        data = self.search_data()
        for link_add in data:
            # web domain address additional in startswith('/)
            # ex ) naver.com => https://www.naver.com
            total_search = create_url.url_addition(link_add)
            time.sleep(1)
            # click_url(url=total_search)
            visit_site.append(total_search)

    def main_steam(self):
        soup = self.next_page_injection()
        for i in soup:
            self.soup = BeautifulSoup(i, 'html.parser')

            self.search_data()
            self.get_url()