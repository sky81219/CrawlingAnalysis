"""
대규모 크롤링(여러가지 검색 엔진 사이트(google naver bing daum)을 해서 (내가 진행하고있음)
"""
import json
import re
import time
import logging
from threading import Thread
from collections import deque

import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from crawling import database
from phishing_spark.phishing_preprocessing.phishing import PhishingPreprocessing

# 방문 큐 만들기 설계 진행해야함
visit_site = deque()
visited_site = deque()
# expected_site = deque()

request_except = requests.exceptions
url_except = urllib3.exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# database
insert_base = database.MysqlConnect()

"""
thread
  ▲
UrlParsing
  ▲
Sele
"""
# 스레드 적용해보기
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

                # url 합성
                total_url = self.url_addition(get_link)

                # log
                logging.info(f'link -> {total_url}, title -> {get_text},  status_code -> {status}')
                tag = self.count_tag_url()

                # JSON 생산
                self.making_json_file(total_url, get_text, status, tag)

                # 큐 설정
                visit_site.append(total_url)
                while visit_site:
                    node = visit_site.popleft()
                    if node not in visited_site:
                        visited_site.append(node)

                # db insert
                # insert_base.url_tag_db_insert(total_url, get_text, tag[0], tag[1], tag[2], tag[3])
                # insert_base.url_status_db_insert(total_url, status, get_text, tag[0], tag[2])

        except (request_except.ConnectionError, url_except.MaxRetryError, url_except.ProtocolError,
                url_except.NewConnectionError):
            print('Error or schemaMissing')

    def count_tag_url(self):
        a_count = [a_tag for a_tag in self.soup.find_all('a')]
        a_href = [0 if a_tag == KeyError else a_tag.href for a_tag in self.soup.find_all('a')]
        link_count = [a_tag for a_tag in self.soup.find_all('link')]
        link_href = [0 if a_tag == KeyError else a_tag.href for a_tag in self.soup.find_all('link')]

        return int(len(a_count)), int(len(a_href)), int(len(link_count)), int(len(link_href))

    # json 파일 만들기
    @staticmethod
    def making_json_file(total_url, get_text, status, tag):
        # json 파일규격
        data_architecture = {"url": total_url,
                             "title": get_text,
                             "status_code": status,
                             "tag": {
                                     "a_tag": tag[0],
                                     "a_href": tag[1],
                                     "line_tag": tag[2],
                                     "link_href": tag[3]
                                     }
                             }
        json.dumps(data_architecture, indent=4)

    @staticmethod
    # phishing 특징 추출
    def phishing_prepro():
        print(f"{int(len(visited_site))}개의 URL 를 수집 했습니다 Phishing site feature 추출을 시작합니다")
        for data in visited_site:
            PhishingPreprocessing(data).making_data()

    def main_stream(self, html_data):
        self.soup = BeautifulSoup(html_data, "lxml")
        self.search_data()
        self.phishing_prepro()

"""
def th_main():
    print("시작합니다")
    th = threading.Thread(target=UrlParsingDriver, args=())
    th.setDaemon(True)
    th.start()
    th.join()
"""
