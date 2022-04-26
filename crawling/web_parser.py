"""
대규모 크롤링(여러가지 검색 엔진 사이트(google naver bing daum)을 해서 (내가 진행하고있음)
"""
import json
import re
import time
import logging
from collections import deque

import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from crawling import database
from crawling.selenium_util import GoogleSeleniumUtility


# 방문 큐 만들기 설계 진행해야함
visit_site = deque()
visited_site = deque()
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

뭔가 빡세게 못짯음 
"""

def page_invest(url):
    # 큐 설정
    visit_site.append(url)
    while visit_site:
        node = visit_site.popleft()
        if node not in visited_site:
            visited_site.append(node)
            return visited_site


def url_create(url):
    return f'{urlparse(url).scheme}://{urlparse(url).netloc}/'

# /~ 로 끝나는 url 붙여주는 함수
def url_addition(url):
    link = url_create(url) + url if url.startswith('/') else url
    return link


# 스레드 적용해보기
class UrlParsingDriver(GoogleSeleniumUtility):
    def __init__(self, count=3, data=None):
        super().__init__(count, data)
        self.ignore_tag = '#'
        self.ignore_url = re.compile('^(http|https)+://(webcache)')
        self.ignore_search = re.compile('^/(search)|(related:)')
        self.soup = None

    def google_search_data(self):
        if self.soup is None:
            return
        # a tag -> h3 tag location
        # GoogleSeleniumUtility 상속
        try:
            get_url = []
            # google search div box <div id='rso'>
            for a_tag in self.soup.find('div', id='rso').find_all('a'):
                # href data 수집
                get_link = a_tag['href']
                get_text = a_tag.text
                time.sleep(1)

                if self.ignore_url.findall(get_link) or self.ignore_search.findall(get_link):
                    continue
                if self.ignore_tag == get_link:
                    continue

                # url 합성
                total_url = url_addition(get_link)

                # web page status code 200 ~ 405
                status = requests.get(total_url, verify=False).status_code
                time.sleep(1)

                logging.info(f'link -> {total_url} || title -> {get_text} || status_code -> {status}')

                # JSON 생성
                self.making_json_file(total_url, get_text, status)
                get_url.append(total_url)

            return get_url

        except (request_except.ConnectionError, url_except.MaxRetryError, url_except.ProtocolError,
                url_except.NewConnectionError):
            print('Error or schemaMissing')

    def main_stream(self):
        url_data = []
        html = self.page()
        for i in html:
            self.soup = BeautifulSoup(i, "lxml")
            data = self.google_search_data()
            url_data.append(data)
            # self.phishing_prepro()
        return url_data

    # json 파일 만들기
    @staticmethod
    def making_json_file(total_url, get_text, status):
        # json 파일규격
        data_architecture = {"url": total_url,
                             "title": get_text,
                             "status_code": status}
        json.dumps(data_architecture, indent=4)
    """
    @staticmethod
    # phishing 특징 추출
    def phishing_prepro():
        print(f"{int(len(visited_site))}개의 URL 를 수집 했습니다 Phishing site feature 추출을 시작합니다")
        for data in visited_site:
            PhishingPreprocessing(data).making_data()
    """

# 셀레니움에서 url 를 받으면 url 속에 html 을 가져오기
class HtmlPageInvestigation(UrlParsingDriver):
    def __init__(self, count=3, data=None, url="https://www.google.com"):
        super().__init__(count, data)
        self.soup = None

    def url_html(self):
        url_html = []
        url = self.main_stream()
        for url_data in url:
            for i in url_data:
                url_html.append(i)

        return url_html

    # soup 통합 할 수 있음 일단 완성이 목표여서 완성하고 리팩토링 진행
    def html_search(self):
        source = self.url_html()
        for data in source:
            req = requests.get(data).content
            self.soup = BeautifulSoup(req)
            for url_href in self.soup.find_all("a"):
                href = url_href.get("href")
                print(href)

                # tag = self.count_tag_url()

                # db insert
                # insert_base.url_tag_db_insert(total_url, get_text, tag[0], tag[1], tag[2], tag[3])
                # insert_base.url_status_db_insert(total_url, status, get_text, tag[0], tag[2])

    def count_tag_url(self):
        a_count = [a_tag for a_tag in self.soup.find_all('a')]
        a_href = [0 if a_tag == KeyError else a_tag.href for a_tag in self.soup.find_all('a')]
        link_count = [a_tag for a_tag in self.soup.find_all('link')]
        link_href = [0 if a_tag == KeyError else a_tag.href for a_tag in self.soup.find_all('link')]

        return int(len(a_count)), int(len(a_href)), int(len(link_count)), int(len(link_href))


class DriverUtility(HtmlPageInvestigation, GoogleSeleniumUtility):
    # 생성자 설정
    def __init__(self, count, data):
        super().__init__(count, data)
        self.data = data
        self.count = count

    def start(self):
        self.html_search()