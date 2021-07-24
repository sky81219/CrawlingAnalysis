"""
대규모 크롤링(여러가지 검색 엔진 사이트(google naver bing daum)을 해서 (내가 진행하고있음)
"""
import logging
import re
import threading
from queue import Queue

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from Crawling.core_parsing.utility import GoogleSeleniumUtility


def queue_data():
    visit_site = Queue()
    visited_site = Queue()
    expected_site = Queue()


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
class UrlParsingDriver(GoogleSeleniumUtility):
    def __init__(self, data, count=2):
        super(UrlParsingDriver, self).__init__(data=data, count=count)
        self.ignore_tag = '#'
        self.ignore_url = re.compile('^(http|https)+://(webcache)')
        self.ignore_search = re.compile('^/(search)|(related:)')

    def search_data(self):
        # a tag -> h3 tag location
        for html_data in self.next_page_injection():
            soup = BeautifulSoup(html_data, 'html.parser')
            for a_tag in soup.find('div', id='rso').find_all('a'):
                get_link = a_tag['href']
                req = requests.get(get_link).status_code
                logging.info(f'link -> {get_link}, status_code -> {req}')

                if self.ignore_url.findall(get_link) or self.ignore_search.findall(get_link):
                    continue
                if self.ignore_tag == get_link:
                    continue

                if get_link is not None:
                    total_search = create_url.url_addition(get_link)
                    print(total_search)

            for h3_tag in soup.find_all('h3', {'class': 'LC20lb DKV0Md'}):
                text_data = h3_tag.text
                print(text_data)
