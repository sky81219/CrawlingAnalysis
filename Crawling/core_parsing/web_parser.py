from core_parsing.utility import GoogleSeleniumUtility as SU

from bs4 import BeautifulSoup
from urllib.parse import urlparse


# html data paring
class UrlParsingDriver(SU):
    def __init__(self, data=None, count=5, url='https://google.com'):
        super(UrlParsingDriver, self).__init__(data=data, count=count, url=url)
        self.ignore_tag = '#' or 'javascript'
        self.data = data
        self.url = self.url

        self.url_box = []
        self.text_box = []

    # URL 스키마 잠금 함수
    def url_create(self):
        return f'{urlparse(self.url).scheme}://{urlparse(self.url).netloc}/'

    # /~ 로 끝나는 url 붙여주는 함수
    def url_addition(self, url):
        link = self.url_create() + url if url.startswith('/') else url
        return link

    def search_data(self):
        # 시작 코드
        for href_data in self.next_page_injection():
            soup = BeautifulSoup(href_data, 'lxml')
            # a tag -> h3 tag location
            for a_tag in soup.find('div', id='rso').find_all('a'):
                get_link = a_tag['href']
                if get_link == self.ignore_tag:
                    continue

                if get_link is not None:
                    total_search = self.url_addition(get_link)

            for h3_tag in soup.find_all('h3', {'class': 'LC20lb DKV0Md'}):
                text_data = h3_tag.text
                print(text_data)
